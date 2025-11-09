"""The ``Site`` is the top of the Storytime catalog."""

from storytime import get_certain_callable, PACKAGE_DIR


def test_package_dir() -> None:
    """Ensure the top of the package is found as a path."""
    assert PACKAGE_DIR.name == "storytime"
    assert PACKAGE_DIR.is_dir()


def test_get_certain_callable() -> None:
    """Given a module, find the function that returns a certain type."""
    from examples.minimal.components import stories

    section = get_certain_callable(stories)
    if section:
        assert section.title == "Components"


def test_no_callable() -> None:
    """This example does not have a function with correct return type."""
    from examples.no_sections.components import stories

    section = get_certain_callable(stories)
    assert section is None
