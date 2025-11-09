"""The ``Site`` for stories used for the Storytime UI itself."""

from storytime import Site
from storytime import components
from storytime import make_site


def this_site() -> Site:
    """The top of the Storytime UI story catalog."""
    return Site(
        scannables=[
            components,
        ],
        title="Storytime UI",
    )


def test_storytime_ui() -> None:
    """Ensure this example works."""
    site = make_site("storytime")
    section = site.items["components"]
    subject = section.items["index"]
    story = subject.stories[0]
    assert story.title == "Index Page Story"
    assert story.vdom.tag == "div"
    soup = story.soup.select_one("div")
    assert soup.text == "Index Page, bazinga"
