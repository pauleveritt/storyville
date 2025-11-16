"""Called by the CLI main to build the site to disk."""


from pathlib import Path
from shutil import copytree, rmtree

from storytime.section.views import SectionView
from storytime.site.views import SiteView
from storytime.stories import make_site
from storytime.subject.views import SubjectView


def build_site(package_location: str, output_dir: Path) -> None:
    """Write the static files and story info to the output directory.

    Args:
        package_location: The package location to build from
        output_dir: The output directory to write the built site to

    The builder:
    1. Clears the output directory if it exists and is not empty
    2. Creates a site from the package location
    3. Walks the tree and renders each view to disk as index.html
    4. Copies static assets from layout to output/static
    """

    # Clear output directory if it exists and is not empty
    if output_dir.exists():
        # Remove all contents
        for item in output_dir.iterdir():
            if item.is_dir():
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

    # Walk the tree and render each section and subject
    for section_key, section in site.items.items():
        # Create section directory
        section_dir = output_dir / "section" / section_key
        section_dir.mkdir(parents=True, exist_ok=True)

        # Render section index page
        section_view = SectionView(section=section, site=site)
        section_html = section_view()
        with open(section_dir / "index.html", "w") as f:
            section_output = str(section_html)
            f.write(section_output)

        # Walk subjects in this section
        for subject_key, subject in section.items.items():
            # Create subject directory
            subject_dir = section_dir / subject_key
            subject_dir.mkdir(parents=True, exist_ok=True)

            # Render subject index page
            subject_view = SubjectView(subject=subject, site=site)
            subject_html = subject_view()
            with open(subject_dir / "index.html", "w") as f:
                subject_output = str(subject_html)
                f.write(subject_output)

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
