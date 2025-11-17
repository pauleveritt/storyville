"""Tests for AboutView component."""

from typing import cast

from tdom import Element, Fragment, Node

from storytime.site.models import Site
from storytime.views.about_view import AboutView


def _get_element(result: Node) -> Element:
    """Extract Element from result (handles Fragment wrapper)."""
    if isinstance(result, Fragment):
        # Fragment contains the html element as first child
        for child in result.children:
            if isinstance(child, Element):
                return child
        raise ValueError("No Element found in Fragment")
    return cast(Element, result)


def test_about_view_renders_with_layout():
    """AboutView should render and wrap content in Layout."""
    # Arrange
    site = Site(title="Test Site")
    view = AboutView(site=site)

    # Act
    result = view()

    # Assert - result should be an Element with html tag
    element = _get_element(result)
    assert element.tag == "html"


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

    # Assert - depth=0 means ../static/ for CSS paths
    assert '../static/pico-main.css' in html_string
