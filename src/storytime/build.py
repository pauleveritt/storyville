"""Called by the CLI main to build the site to disk."""


from pathlib import Path
from shutil import copytree, rmtree

from storytime.section.views import SectionView
from storytime.site.views import SiteView
from storytime.stories import make_site
from storytime.story.views import StoryView
from storytime.subject.views import SubjectView
from storytime.views.about_view import AboutView
from storytime.views.debug_view import DebugView


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
    site_view = SiteView(site=site)
    index_html = site_view()
    with open(output_dir / "index.html", "w") as f:
        index_output = str(index_html)
        f.write(index_output)

    # Render the About page
    about_view = AboutView(site=site)
    about_html = about_view()
    with open(output_dir / "about.html", "w") as f:
        about_output = str(about_html)
        f.write(about_output)

    # Render the Debug page
    debug_view = DebugView(site=site)
    debug_html = debug_view()
    with open(output_dir / "debug.html", "w") as f:
        debug_output = str(debug_html)
        f.write(debug_output)

    # Walk the tree and render each section and subject
    for section_key, section in site.items.items():
        # Create section directory (no "section" prefix)
        section_dir = output_dir / section_key
        section_dir.mkdir(parents=True, exist_ok=True)

        # Render section index page
        section_view = SectionView(section=section, site=site)
        section_html = section_view()
        with open(section_dir / "index.html", "w") as f:
            section_output = str(section_html)
            f.write(section_output)

        # Walk subjects in this section
        for subject_key, subject in section.items.items():
            # Create subject directory (no "subject" prefix)
            subject_dir = section_dir / subject_key
            subject_dir.mkdir(parents=True, exist_ok=True)

            # Render subject index page
            subject_view = SubjectView(subject=subject, site=site)
            subject_html = subject_view()
            with open(subject_dir / "index.html", "w") as f:
                subject_output = str(subject_html)
                f.write(subject_output)

            # Walk stories in this subject
            for story_idx, story in enumerate(subject.items):
                # Create story directory
                story_dir = subject_dir / f"story-{story_idx}"
                story_dir.mkdir(parents=True, exist_ok=True)

                # Render story index page
                story_view = StoryView(story=story, site=site)
                story_html = story_view()
                with open(story_dir / "index.html", "w") as f:
                    story_output = str(story_html)
                    f.write(story_output)

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
