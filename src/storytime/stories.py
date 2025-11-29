"""The ``Catalog`` for stories used for the Storytime UI itself."""


from storytime import Catalog, make_catalog


def this_catalog() -> Catalog:
    """The top of the Storytime UI story catalog."""
    return Catalog(
        title="Storytime UI",
    )


def test_storytime_ui() -> None:
    """Ensure this example works."""
    catalog = make_catalog("storytime")
    section = catalog.items["components"]
    subject = section.items["index"]
    story = subject.items[0]
    assert story.title == "Index Page Story"
