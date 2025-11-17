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


@pytest.fixture(autouse=True)
def cleanup_websocket_loop():
    """Clean up websocket globals after each test.

    We avoid touching the event loop or its policy here because pytest-anyio
    manages an `asyncio.Runner` per test. Closing or resetting the loop/policy
    during teardown can race with the plugin's own cleanup and produce
    "Runner is closed" or nested-loop errors.
    """
    yield

    # After test completes, clear any stale websocket globals only
    from storytime import websocket
    websocket._websocket_loop = None
    websocket._active_connections.clear()


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    """Run watchers tests first to avoid interference from other async plugins/tests."""
    def sort_key(it: pytest.Item) -> tuple[int, str]:
        nodeid = it.nodeid
        priority = 0 if "tests/test_watchers.py::" in nodeid or nodeid.startswith("tests/test_watchers.py") else 1
        return (priority, nodeid)

    items.sort(key=sort_key)


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


# Async watcher test fixtures
@pytest.fixture
def watcher_runner():
    """Factory for running watchers with automatic lifecycle management.

    Returns an async context manager that handles watcher task creation,
    startup delay, and cleanup on exit.

    Example:
        async def test_something(watcher_runner):
            async with watcher_runner(watch_and_rebuild, ...) as task:
                # Watcher is running
                # Do test operations
                pass
            # Watcher is stopped and cleaned up
    """
    from contextlib import asynccontextmanager
    import asyncio

    @asynccontextmanager
    async def run(watcher_func, **kwargs):
        """Run a watcher function with automatic lifecycle management.

        Args:
            watcher_func: The watcher function to run (e.g., watch_and_rebuild)
            **kwargs: Arguments to pass to the watcher function

        Yields:
            asyncio.Task: The running watcher task
        """
        task = asyncio.create_task(watcher_func(**kwargs))
        # Give watcher time to start
        await asyncio.sleep(0.5)
        try:
            yield task
        finally:
            # Clean up watcher
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass

    return run
