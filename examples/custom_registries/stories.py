"""A storytime site with a custom registry."""
from hopscotch import Registry

from storytime import make_site
from storytime import Site

context = dict(title="Custom Registries Site")
registry = Registry(context=context)


def this_site() -> Site:
    """The top of this package's story catalog."""
    return Site(
        registry=registry,
        title="Custom Registry",
    )


def test_custom_registries() -> None:
    """Ensure this example works."""
    site = make_site("examples.custom_registries")
    assert site.registry.context["title"] == "Custom Registries Site"
    assert site.registry.parent is None
    section = site.items["components"]
    assert section.registry.parent is None
    assert section.registry.context["title"] == "Custom Registries Section"
