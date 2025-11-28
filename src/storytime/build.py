"""Called by the CLI main to build the site to disk."""

import logging
from pathlib import Path
from shutil import copytree, rmtree
from time import perf_counter

from storytime.components.themed_story import ThemedStory
from storytime.section.views import SectionView
from storytime.site.views import SiteView
from storytime.stories import make_site
from storytime.story.views import StoryView
from storytime.subject.views import SubjectView
from storytime.views.about_view import AboutView
from storytime.views.debug_view import DebugView

logger = logging.getLogger(__name__)


def _write_html(content: str, path: Path) -> None:
    """Write rendered HTML content to file.

    Args:
        content: The rendered HTML string to write
        path: The file path to write to (parent dirs created automatically)
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def build_site(
    package_location: str, output_dir: Path, with_assertions: bool = True
) -> None:
    """Write the static files and story info to the output directory.

    Args:
        package_location: The package location to build from
        output_dir: The output directory to write the built site to
        with_assertions: Whether to execute assertions during rendering (default: True)

    The builder:
    1. Clears the output directory if it exists and is not empty
    2. Creates a site from the package location
    3. Walks the tree and renders each view (site, sections, subjects, stories) to disk as index.html
    4. Renders About and Debug pages
    5. Copies static assets from layout to output/static
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
    site = make_site(package_location=package_location)
    end_reading = perf_counter()
    reading_duration = end_reading - start_reading
    logger.info(f"Phase Reading: completed in {reading_duration:.2f}s")

    # Phase 2: Rendering - Process views and generate HTML
    start_rendering = perf_counter()

    # Generate cached navigation tree once (without current_path highlighting)
    from storytime.components.navigation_tree import NavigationTree

    cached_nav = str(NavigationTree(sections=site.items, current_path=None)())

    # Render the site index page (root) and convert to string
    site_view = str(SiteView(site=site, cached_navigation=cached_nav)())

    # Render the About page and convert to string
    about_view = str(AboutView(site=site, cached_navigation=cached_nav)())

    # Render the Debug page and convert to string
    debug_view = str(DebugView(site=site, cached_navigation=cached_nav)())

    # Walk the tree and render each section and subject
    rendered_sections = []
    rendered_subjects = []
    rendered_stories = []
    rendered_themed_stories = []

    for section_key, section in site.items.items():
        # Render section index page and convert to string
        section_view = str(
            SectionView(section=section, site=site, cached_navigation=cached_nav)()
        )
        rendered_sections.append((section_key, section_view))

        # Walk subjects in this section
        for subject_key, subject in section.items.items():
            # Render subject index page and convert to string
            subject_view = str(
                SubjectView(subject=subject, site=site, cached_navigation=cached_nav)()
            )
            rendered_subjects.append((section_key, subject_key, subject_view))

            # Walk stories in this subject
            for story_idx, story in enumerate(subject.items):
                # Render story index page and convert to string
                # Pass with_assertions flag to StoryView
                story_view = str(
                    StoryView(
                        story=story,
                        site=site,
                        cached_navigation=cached_nav,
                        with_assertions=with_assertions,
                    )()
                )
                rendered_stories.append((section_key, subject_key, story_idx, story_view))

                # Render themed story if site has themed_layout configured
                if site.themed_layout is not None and story.instance is not None:
                    themed_story = ThemedStory(
                        story_title=story.title or "Untitled Story",
                        children=story.instance,
                        site=site
                    )
                    themed_story_html = str(themed_story())
                    rendered_themed_stories.append(
                        (section_key, subject_key, story_idx, themed_story_html)
                    )

    end_rendering = perf_counter()
    rendering_duration = end_rendering - start_rendering
    logger.info(f"Phase Rendering: completed in {rendering_duration:.2f}s")

    # Phase 3: Writing - Write files to disk
    start_writing = perf_counter()

    # Write site pages
    _write_html(site_view, output_dir / "index.html")
    _write_html(about_view, output_dir / "about.html")
    _write_html(debug_view, output_dir / "debug.html")

    # Write sections
    for section_key, section_view in rendered_sections:
        section_dir = output_dir / section_key
        _write_html(section_view, section_dir / "index.html")

    # Write subjects
    for section_key, subject_key, subject_view in rendered_subjects:
        section_dir = output_dir / section_key
        subject_dir = section_dir / subject_key
        _write_html(subject_view, subject_dir / "index.html")

    # Write stories
    for section_key, subject_key, story_idx, story_view in rendered_stories:
        section_dir = output_dir / section_key
        subject_dir = section_dir / subject_key
        story_dir = subject_dir / f"story-{story_idx}"
        _write_html(story_view, story_dir / "index.html")

    # Write themed stories
    for section_key, subject_key, story_idx, themed_story_html in rendered_themed_stories:
        section_dir = output_dir / section_key
        subject_dir = section_dir / subject_key
        story_dir = subject_dir / f"story-{story_idx}"
        _write_html(themed_story_html, story_dir / "themed_story.html")

    # Copy static assets from layout to output/static
    if site.static_dir:
        copytree(site.static_dir, output_dir / "static", dirs_exist_ok=True)

    end_writing = perf_counter()
    writing_duration = end_writing - start_writing
    logger.info(f"Phase Writing: completed in {writing_duration:.2f}s")

    # Log total build time
    total_duration = reading_duration + rendering_duration + writing_duration
    logger.info(f"Build completed in {total_duration:.2f}s")


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print("Usage: python -m storytime.build <input> <output>", file=sys.stderr)
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = Path(sys.argv[2])

    print(f"Building site from '{input_path}' to '{output_path}'...")
    build_site(package_location=input_path, output_dir=output_path)
    print("Build complete!")
