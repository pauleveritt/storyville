"""Custom registry examples in a `Section`."""
from hopscotch import Registry

from storytime import Section

context = dict(title="Custom Registries Section")
registry = Registry(context=context)


def this_section() -> Section:
    """Let's make a Storytime section for Components."""
    return Section(
        registry=registry,
        title="Components",
    )
