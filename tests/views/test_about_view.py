"""Tests for AboutView component."""


from aria_testing import get_by_tag_name
from storytime.site.models import Site
from storytime.views.about_view import AboutView

def test_about_view_renders_with_layout():
    """AboutView should render and wrap content in Layout."""
    # Arrange
    site = Site(title="Test Site")
    view = AboutView(site=site)

    # Act
    result = view()

    # Assert - result should contain an html element
    element = result
    html_elem = get_by_tag_name(element, "html")
    assert html_elem is not None

def test_about_view_has_correct_title():
    """AboutView should have 'About' as view_title."""
    # Arrange
    site = Site(title="My Site")
    view = AboutView(site=site)

    # Act
    result = view()
    html_string = str(result)

    # Assert - title should be "About - My Site"
    assert "<title>About - My Site</title>" in html_string

def test_about_view_has_about_heading():
    """AboutView should render an h1 with 'About' heading."""
    # Arrange
    site = Site(title="Test Site")
    view = AboutView(site=site)

    # Act
    result = view()
    html_string = str(result)

    # Assert
    assert "<h1>About Storytime</h1>" in html_string

def test_about_view_uses_depth_zero():
    """AboutView should use depth=0 for root-level view."""
    # Arrange
    site = Site(title="Test Site")
    view = AboutView(site=site)

    # Act
    result = view()
    html_string = str(result)

    # Assert - depth=0 means ../storytime_static/ for CSS paths
    assert '../storytime_static/components/layout/static/pico-main.css' in html_string
