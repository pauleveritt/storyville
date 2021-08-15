"""A storytime site with singletons."""
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


def test_singletons() -> None:
    """Ensure this example works."""
    site = make_site("examples.singletons")
    section = site.items["components"]
    subject0 = section.items["heading"]
    story0 = subject0.stories[0]
    div0 = story0.soup.select_one("div")
    assert div0.text == "Hello !"
    subject1 = section.items["another_heading"]
    story1 = subject1.stories[0]
    div1 = story1.soup.select_one("div")
    assert div1.text == "Howdy ..."
