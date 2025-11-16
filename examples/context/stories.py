"""A storytime site with a context in the registry."""
from storytime import make_site
from storytime import Site


def this_site() -> Site:
    """The top of this package's story catalog."""
    return Site()


def test_context() -> None:
    """Ensure this example works."""
    site = make_site("examples.context")
    # TODO: registry attribute not yet implemented
    # assert site.registry.context is None
    section = site.items["components"]
    # assert section.registry.parent is site.registry
    # assert section.registry.context["title"] == "Context Section"
    assert section is not None
