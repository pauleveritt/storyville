"""The ``Catalog`` for stories used for the Storyville UI itself."""

from storyville import Catalog, make_catalog


def this_catalog() -> Catalog:
    """The top of the Storyville UI story catalog."""
    return Catalog(
        title="Storyville UI",
    )


def test_storyville_ui() -> None:
    """Ensure this example works."""
    catalog = make_catalog("storyville")
    section = catalog.items["components"]
    subject = section.items["index"]
    story = subject.items[0]
    assert story.title == "Index Page Story"
