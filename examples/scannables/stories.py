"""A storytime site with scannables."""
from hopscotch import Registry

from storytime import make_site
from storytime import Site

registry = Registry()


def this_site() -> Site:
    """The top of this package's story catalog."""
    return Site(
        registry=registry,
        title="Scannables",
    )


def test_scannables() -> None:
    """Ensure this example works."""
    site = make_site("examples.scannables")
    section = site.items["components"]
    subject = section.items["heading"]
    story = subject.stories[0]
    assert getattr(story.instance, "title") == "Some Heading"
    div = story.soup.select_one("div")
    assert div.text == "Hello Some Heading"
