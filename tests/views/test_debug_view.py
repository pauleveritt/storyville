"""Tests for DebugView component."""


from aria_testing import get_by_tag_name
from storytime.site.models import Site
from storytime.views.debug_view import DebugView

def test_debug_view_renders_with_layout():
    """DebugView should render and wrap content in Layout."""
    # Arrange
    site = Site(title="Test Site")
    view = DebugView(site=site)

    # Act
    result = view()

    # Assert - result should contain an html element
    element = result
    html_elem = get_by_tag_name(element, "html")
    assert html_elem is not None

def test_debug_view_has_correct_title():
    """DebugView should have 'Debug' as view_title."""
    # Arrange
    site = Site(title="My Site")
    view = DebugView(site=site)

    # Act
    result = view()
    html_string = str(result)

    # Assert - title should be "Debug - My Site"
    assert "<title>Debug - My Site</title>" in html_string

def test_debug_view_has_debug_heading():
    """DebugView should render an h1 with 'Debug' heading."""
    # Arrange
    site = Site(title="Test Site")
    view = DebugView(site=site)

    # Act
    result = view()
    html_string = str(result)

    # Assert
    assert "<h1>Debug Information</h1>" in html_string

def test_debug_view_uses_depth_zero():
    """DebugView should use depth=0 for root-level view."""
    # Arrange
    site = Site(title="Test Site")
    view = DebugView(site=site)

    # Act
    result = view()
    html_string = str(result)

    # Assert - depth=0 means static/ (no prefix) for CSS paths at root
    assert 'static/pico-main.css' in html_string
