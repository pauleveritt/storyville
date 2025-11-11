"""Test utility functions."""

from types import ModuleType

from storytime.site import Site
from storytime.story import Section, Subject
from storytime.utils import get_certain_callable


def test_get_certain_callable_with_site() -> None:
    """Test get_certain_callable finds and calls Site function."""
    # Create a mock module
    module = ModuleType("test_module")

    # Add a function that returns Site
    def make_site() -> Site:
        return Site(title="Test Site")

    # Make it look like it's from this module
    make_site.__module__ = "test_module"
    setattr(module, "make_site", make_site)

    result = get_certain_callable(module)

    assert result is not None
    assert isinstance(result, Site)
    assert result.title == "Test Site"


def test_get_certain_callable_with_section() -> None:
    """Test get_certain_callable finds and calls Section function."""
    module = ModuleType("test_module")

    def make_section() -> Section:
        return Section(title="Test Section")

    make_section.__module__ = "test_module"
    setattr(module, "make_section", make_section)

    result = get_certain_callable(module)

    assert result is not None
    assert isinstance(result, Section)
    assert result.title == "Test Section"


def test_get_certain_callable_with_subject() -> None:
    """Test get_certain_callable finds and calls Subject function."""
    module = ModuleType("test_module")

    def make_subject() -> Subject:
        return Subject(title="Test Subject")

    make_subject.__module__ = "test_module"
    setattr(module, "make_subject", make_subject)

    result = get_certain_callable(module)

    assert result is not None
    assert isinstance(result, Subject)
    assert result.title == "Test Subject"


def test_get_certain_callable_no_matching_function() -> None:
    """Test get_certain_callable returns None when no matching function."""
    module = ModuleType("test_module")

    # Add a function with wrong return type
    def make_something() -> str:
        return "something"

    make_something.__module__ = "test_module"
    setattr(module, "make_something", make_something)

    result = get_certain_callable(module)

    assert result is None


def test_get_certain_callable_empty_module() -> None:
    """Test get_certain_callable returns None for empty module."""
    module = ModuleType("test_module")

    result = get_certain_callable(module)

    assert result is None


def test_get_certain_callable_ignores_external_functions() -> None:
    """Test get_certain_callable ignores functions from other modules."""
    module = ModuleType("test_module")

    # Add a function from a different module
    def external_function() -> Site:
        return Site(title="External")

    external_function.__module__ = "other_module"  # Different module!
    setattr(module, "external_function", external_function)

    result = get_certain_callable(module)

    assert result is None  # Should not call external functions


def test_get_certain_callable_integration_minimal_components() -> None:
    """Integration: use a real example module returning a Section."""
    from examples.minimal.components import stories

    section = get_certain_callable(stories)
    if section:
        assert section.title == "Components"


def test_get_certain_callable_integration_no_sections() -> None:
    """Integration: real example module without a matching callable returns None."""
    from examples.no_sections.components import stories

    section = get_certain_callable(stories)
    assert section is None
