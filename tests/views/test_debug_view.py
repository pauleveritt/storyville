"""Tests for DebugView component."""


from aria_testing import get_by_tag_name
from storytime.catalog.models import Catalog
from storytime.views.debug_view import DebugView

def test_debug_view_renders_with_layout():
    """DebugView should render and wrap content in Layout."""
    # Arrange
    catalog = Catalog(title="Test Catalog")
    view = DebugView(site=catalog)

    # Act
    result = view()

    # Assert - result should contain an html element
    element = result
    html_elem = get_by_tag_name(element, "html")
    assert html_elem is not None

def test_debug_view_has_correct_title():
    """DebugView should have 'Debug' as view_title."""
    # Arrange
    catalog = Catalog(title="My Catalog")
    view = DebugView(site=catalog)

    # Act
    result = view()
    html_string = str(result)

    # Assert - title should be "Debug - My Catalog"
    assert "<title>Debug - My Catalog</title>" in html_string

def test_debug_view_has_debug_heading():
    """DebugView should render an h1 with 'Debug' heading."""
    # Arrange
    catalog = Catalog(title="Test Catalog")
    view = DebugView(site=catalog)

    # Act
    result = view()
    html_string = str(result)

    # Assert
    assert "<h1>Debug Information</h1>" in html_string

def test_debug_view_uses_depth_zero():
    """DebugView should use depth=0 for root-level view."""
    # Arrange
    catalog = Catalog(title="Test Catalog")
    view = DebugView(site=catalog)

    # Act
    result = view()
    html_string = str(result)

    # Assert - depth=0 means static/ (no prefix) for CSS paths at root with full nested path
    assert 'static/components/layout/static/pico-main.css' in html_string
