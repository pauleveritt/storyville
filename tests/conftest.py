"""Pytest configuration and fixtures."""

import sys
from dataclasses import dataclass
from pathlib import Path
from types import ModuleType
from unittest.mock import MagicMock

import pytest
from tdom import Node, html

# Add examples directory to sys.path so tests can import from it
examples_path = Path(__file__).parent.parent / "examples"
if str(examples_path) not in sys.path:
    sys.path.insert(0, str(examples_path.parent))


# Common test component fixtures
@pytest.fixture
def my_component():
    """A simple test component with name field."""
    @dataclass
    class MyComponent:
        name: str = "test"
    return MyComponent


@pytest.fixture
def parent_component():
    """A test component representing a parent with name field."""
    @dataclass
    class ParentComponent:
        name: str = "parent"
    return ParentComponent


@pytest.fixture
def own_component():
    """A test component representing ownership with name field."""
    @dataclass
    class OwnComponent:
        name: str = "own"
    return OwnComponent


@pytest.fixture
def another_component():
    """A test component with label field instead of name."""
    @dataclass
    class AnotherComponent:
        label: str = "default"
    return AnotherComponent


@pytest.fixture
def simple_view():
    """A simple view component for testing View protocol."""
    @dataclass
    class SimpleView:
        def __call__(self) -> Node:
            return html(t"<div>Hello</div>")
    return SimpleView


@pytest.fixture
def element_view():
    """An element view component for testing View protocol."""
    @dataclass
    class ElementView:
        def __call__(self) -> Node:
            return html(t"<p>Content</p>")
    return ElementView


@pytest.fixture
def field_view():
    """A view component with fields for testing View protocol."""
    @dataclass
    class FieldView:
        title: str = "Test"

        def __call__(self) -> Node:
            return html(t"<h1>{self.title}</h1>")
    return FieldView


# Test helper factories
@pytest.fixture
def mock_tree_node():
    """Factory for creating mock tree nodes.

    Returns a function that creates mock TreeNode objects with
    configurable name and package_location attributes.

    Example:
        def test_something(mock_tree_node):
            tree_node = mock_tree_node(name="components", package_location=".components")
            assert tree_node.name == "components"
    """
    def _create(name: str = "root", package_location: str = "."):
        tree_node = MagicMock()
        tree_node.name = name
        tree_node.this_package_location = package_location
        return tree_node
    return _create


@pytest.fixture
def module_factory():
    """Factory for creating test modules with callables.

    Returns a function that creates ModuleType instances with optional
    callable functions that have proper __module__ attributes set.

    Example:
        def test_something(module_factory):
            def my_func() -> Site:
                return Site(title="Test")
            module = module_factory("test_module", my_func)
    """
    def _create(module_name: str = "test_module", callable_func=None):
        module = ModuleType(module_name)
        if callable_func:
            callable_func.__module__ = module_name
            setattr(module, callable_func.__name__, callable_func)
        return module
    return _create
