"""Called by the CLI main to build the catalog to disk."""

import logging
from pathlib import Path
from shutil import rmtree
from time import perf_counter
from typing import TYPE_CHECKING

from storytime import PACKAGE_DIR
from storytime.catalog.views import CatalogView
from storytime.components.themed_story import ThemedStory
from storytime.section.views import SectionView
from storytime.static_assets import copy_all_static_assets
from storytime.stories import make_catalog
from storytime.story.views import StoryView
from storytime.subject.views import SubjectView
from storytime.views.about_view import AboutView
from storytime.views.debug_view import DebugView

if TYPE_CHECKING:
    from storytime.catalog import Catalog

logger = logging.getLogger(__name__)


def _render_all_views(
    catalog: "Catalog", with_assertions: bool
) -> tuple[str, str, str, list, list, list, list]:
    """Render all views to HTML strings.

    Args:
        catalog: The catalog to render
        with_assertions: Whether to execute assertions during rendering

    Returns:
        Tuple of (catalog_view, about_view, debug_view, rendered_sections,
                 rendered_subjects, rendered_stories, rendered_themed_stories)
    """
    from storytime.components.navigation_tree import NavigationTree

    cached_nav = str(NavigationTree(sections=catalog.items, current_path=None)())

    # Render the catalog index page (root) and convert to string
    catalog_view = str(CatalogView(catalog=catalog, cached_navigation=cached_nav)())

    # Render the About page and convert to string
    about_view = str(AboutView(site=catalog, cached_navigation=cached_nav)())

    # Render the Debug page and convert to string
    debug_view = str(DebugView(site=catalog, cached_navigation=cached_nav)())

    # Walk the tree and render each section and subject
    rendered_sections = []
    rendered_subjects = []
    rendered_stories = []
    rendered_themed_stories = []

    for section_key, section in catalog.items.items():
        # Render section index page and convert to string
        section_view = str(
            SectionView(section=section, site=catalog, cached_navigation=cached_nav)()
        )
        rendered_sections.append((section_key, section_view))

        # Walk subjects in this section
        for subject_key, subject in section.items.items():
            # Render subject index page and convert to string
            subject_view = str(
                SubjectView(subject=subject, site=catalog, cached_navigation=cached_nav)()
            )
            rendered_subjects.append((section_key, subject_key, subject_view))

            # Walk stories in this subject
            for story_idx, story in enumerate(subject.items):
                # Render story index page and convert to string
                # Pass with_assertions flag to StoryView
                story_view = str(
                    StoryView(
                        story=story,
                        site=catalog,
                        cached_navigation=cached_nav,
                        with_assertions=with_assertions,
                    )()
                )
                rendered_stories.append((section_key, subject_key, story_idx, story_view))

                # Render themed story if catalog has themed_layout configured
                if catalog.themed_layout is not None and story.instance is not None:
                    themed_story = ThemedStory(
                        story_title=story.title or "Untitled Story",
                        children=story.instance,
                        site=catalog
                    )
                    themed_story_html = str(themed_story())
                    rendered_themed_stories.append(
                        (section_key, subject_key, story_idx, themed_story_html)
                    )

    return (
        catalog_view,
        about_view,
        debug_view,
        rendered_sections,
        rendered_subjects,
        rendered_stories,
        rendered_themed_stories,
    )


def _write_all_files(
    output_dir: Path,
    catalog_view: str,
    about_view: str,
    debug_view: str,
    rendered_sections: list,
    rendered_subjects: list,
    rendered_stories: list,
    rendered_themed_stories: list,
) -> None:
    """Write all rendered HTML files to disk.

    Args:
        output_dir: The output directory
        catalog_view: Rendered catalog index page
        about_view: Rendered about page
        debug_view: Rendered debug page
        rendered_sections: List of (section_key, section_view) tuples
        rendered_subjects: List of (section_key, subject_key, subject_view) tuples
        rendered_stories: List of (section_key, subject_key, story_idx, story_view) tuples
        rendered_themed_stories: List of (section_key, subject_key, story_idx, themed_story_html) tuples
    """
    # Write catalog pages
    (output_dir / "index.html").parent.mkdir(parents=True, exist_ok=True)
    (output_dir / "index.html").write_text(catalog_view)
    (output_dir / "about.html").parent.mkdir(parents=True, exist_ok=True)
    (output_dir / "about.html").write_text(about_view)
    (output_dir / "debug.html").parent.mkdir(parents=True, exist_ok=True)
    (output_dir / "debug.html").write_text(debug_view)

    # Write sections
    for section_key, section_view in rendered_sections:
        section_dir = output_dir / section_key
        path = section_dir / "index.html"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(section_view)

    # Write subjects
    for section_key, subject_key, subject_view in rendered_subjects:
        section_dir = output_dir / section_key
        subject_dir = section_dir / subject_key
        path = subject_dir / "index.html"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(subject_view)

    # Write stories
    for section_key, subject_key, story_idx, story_view in rendered_stories:
        section_dir = output_dir / section_key
        subject_dir = section_dir / subject_key
        story_dir = subject_dir / f"story-{story_idx}"
        path = story_dir / "index.html"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(story_view)

    # Write themed stories
    for section_key, subject_key, story_idx, themed_story_html in rendered_themed_stories:
        section_dir = output_dir / section_key
        subject_dir = section_dir / subject_key
        story_dir = subject_dir / f"story-{story_idx}"
        path = story_dir / "themed_story.html"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(themed_story_html)


def build_catalog(
    package_location: str, output_dir: Path, with_assertions: bool = True
) -> None:
    """Write the static files and story info to the output directory.

    Args:
        package_location: The package location to build from
        output_dir: The output directory to write the built catalog to
        with_assertions: Whether to execute assertions during rendering (default: True)

    The builder:
    1. Clears the output directory if it exists and is not empty
    2. Creates a catalog from the package location
    3. Walks the tree and renders each view (catalog, sections, subjects, stories) to disk as index.html
    4. Renders About and Debug pages
    5. Discovers and copies static assets from both src/storytime and input_dir
    """

    # Clear output directory if it exists and is not empty
    if output_dir.exists():
        # Remove all contents
        for item in output_dir.iterdir():
            if item.is_symlink():
                # Skip symlinks (e.g., pytest's "current" links)
                continue
            elif item.is_dir():
                rmtree(item)
            else:
                item.unlink()
    else:
        # Create output directory
        output_dir.mkdir(parents=True, exist_ok=True)

    # Phase 1: Reading - Load content from filesystem
    start_reading = perf_counter()
    catalog = make_catalog(package_location=package_location)
    end_reading = perf_counter()
    reading_duration = end_reading - start_reading
    logger.info(f"Phase Reading: completed in {reading_duration:.2f}s")

    # Phase 2: Rendering - Process views and generate HTML
    start_rendering = perf_counter()

    (
        catalog_view,
        about_view,
        debug_view,
        rendered_sections,
        rendered_subjects,
        rendered_stories,
        rendered_themed_stories,
    ) = _render_all_views(catalog, with_assertions)

    end_rendering = perf_counter()
    rendering_duration = end_rendering - start_rendering
    logger.info(f"Phase Rendering: completed in {rendering_duration:.2f}s")

    # Phase 3: Writing - Write files to disk
    start_writing = perf_counter()

    _write_all_files(
        output_dir,
        catalog_view,
        about_view,
        debug_view,
        rendered_sections,
        rendered_subjects,
        rendered_stories,
        rendered_themed_stories,
    )

    end_writing = perf_counter()
    writing_duration = end_writing - start_writing
    logger.info(f"Phase Writing: completed in {writing_duration:.2f}s")

    # Phase 4: Static Assets - Discover and copy static assets
    start_static = perf_counter()

    # Determine input_dir from package_location
    from importlib.util import find_spec

    spec = find_spec(package_location)
    if spec is None or spec.origin is None:
        # Fallback: treat package_location as file path
        input_dir = Path(package_location).resolve()
        if input_dir.is_file():
            input_dir = input_dir.parent
    else:
        input_dir = Path(spec.origin).parent

    # Copy all static assets from both sources to single static/ directory
    file_count = copy_all_static_assets(
        storytime_base=PACKAGE_DIR,
        input_dir=input_dir,
        output_dir=output_dir,
    )

    end_static = perf_counter()
    static_duration = end_static - start_static
    logger.info(
        f"Phase Static Assets: copied {file_count} files "
        f"in {static_duration:.2f}s"
    )

    # Log total build time
    total_duration = reading_duration + rendering_duration + writing_duration + static_duration
    logger.info(f"Build completed in {total_duration:.2f}s")


# Backward compatibility alias
build_site = build_catalog


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print("Usage: python -m storytime.build <input> <output>", file=sys.stderr)
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = Path(sys.argv[2])

    print(f"Building catalog from '{input_path}' to '{output_path}'...")
    build_catalog(package_location=input_path, output_dir=output_path)
    print("Build complete!")
