"""The ``Site`` for the stories in this package."""
from storytime import make_site
from storytime import Site


def this_site() -> Site:
    """The top of this package's story catalog."""
    return Site(
        title="Minimal Site",
    )


def test_minimal() -> None:
    """Ensure this example works."""
    site = make_site("examples.minimal")
    section = site.items["components"]
    subject = section.items["heading"]
    story = subject.stories[0]
    assert story.title == "Heading Story"
