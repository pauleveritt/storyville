"""Called by the CLI main to build the site to disk."""


from pathlib import Path
from shutil import copytree, rmtree

from tdom import Node

from storytime.section.views import SectionView
from storytime.site.views import SiteView
from storytime.stories import make_site
from storytime.story.views import StoryView
from storytime.subject.views import SubjectView
from storytime.views.about_view import AboutView
from storytime.views.debug_view import DebugView


def _write_html(content: Node, path: Path) -> None:
    """Write rendered HTML content to file.

    Args:
        content: The rendered HTML node to write
        path: The file path to write to (parent dirs created automatically)
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(str(content))


def build_site(package_location: str, output_dir: Path) -> None:
    """Write the static files and story info to the output directory.

    Args:
        package_location: The package location to build from
        output_dir: The output directory to write the built site to

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

    # Make a site and put it in the registry
    site = make_site(package_location=package_location)

    # Render the site index page (root)
    _write_html(SiteView(site=site)(), output_dir / "index.html")

    # Render the About page
    _write_html(AboutView(site=site)(), output_dir / "about.html")

    # Render the Debug page
    _write_html(DebugView(site=site)(), output_dir / "debug.html")

    # Walk the tree and render each section and subject
    for section_key, section in site.items.items():
        # Create section directory (no "section" prefix)
        section_dir = output_dir / section_key

        # Render section index page
        _write_html(SectionView(section=section, site=site)(), section_dir / "index.html")

        # Walk subjects in this section
        for subject_key, subject in section.items.items():
            # Create subject directory (no "subject" prefix)
            subject_dir = section_dir / subject_key

            # Render subject index page
            _write_html(SubjectView(subject=subject, site=site)(), subject_dir / "index.html")

            # Walk stories in this subject
            for story_idx, story in enumerate(subject.items):
                # Create story directory
                story_dir = subject_dir / f"story-{story_idx}"

                # Render story index page
                _write_html(StoryView(story=story, site=site)(), story_dir / "index.html")

    # Copy static assets from layout to output/static
    if site.static_dir:
        copytree(site.static_dir, output_dir / "static", dirs_exist_ok=True)


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
