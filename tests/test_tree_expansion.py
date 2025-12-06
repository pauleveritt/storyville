"""Tests for automatic navigation tree expansion logic."""

from dataclasses import dataclass

from aria_testing import get_by_tag_name, query_all_by_tag_name
from tdom import Node, html

from storyville.catalog.models import Catalog
from storyville.components.layout.layout import Layout
from storyville.section.models import Section
from storyville.story.models import Story
from storyville.subject.models import Subject


@dataclass
class SimpleComponent:
    """A simple test component."""

    name: str = "test"

    def __call__(self) -> Node:
        """Render the component."""
        return html(t"<div>{self.name}</div>")


def test_tree_expand_script_linked_in_layout() -> None:
    """Test that tree-expand.mjs is linked in the Layout component as a module."""
    catalog = Catalog(title="Test Catalog")

    layout = Layout(
        view_title="Test Page",
        site=catalog,
        children=html(t"<div>Test content</div>"),
        depth=0,
    )
    result = layout()

    # Verify result is not None
    assert result is not None

    # Convert to string and check for script tag
    html_str = str(result)
    assert "tree-expand.mjs" in html_str, (
        "tree-expand.mjs script should be linked in layout"
    )
    assert 'type="module"' in html_str, "tree-expand.mjs should be loaded as ES module"


def test_navigation_tree_has_details_elements() -> None:
    """Test that navigation tree contains details elements for expansion."""
    catalog = Catalog(title="Test Catalog")
    section = Section(title="Components", name="components")
    subject = Subject(title="Buttons", name="buttons", target=SimpleComponent)
    Story(title="Primary", parent=subject)

    # Manually build tree structure
    subject.items.append(Story(title="Primary", parent=subject))
    section.items["buttons"] = subject
    catalog.items["components"] = section

    layout = Layout(
        view_title="Test Page",
        site=catalog,
        children=html(t"<div>Test content</div>"),
        depth=0,
        resource_path="components/buttons/story-0",
    )
    result = layout()

    # Verify result is not None
    assert result is not None

    # Get the aside element (sidebar)
    aside = get_by_tag_name(result, "aside")

    # Find all details elements in navigation
    details_elements = query_all_by_tag_name(aside, "details")

    # Should have at least section and subject details
    assert len(details_elements) >= 2, "Navigation should have nested details elements"


def test_navigation_links_have_href_attributes() -> None:
    """Test that navigation links have href attributes for URL matching."""
    catalog = Catalog(title="Test Catalog")
    section = Section(title="Components", name="components")
    subject = Subject(title="Buttons", name="buttons", target=SimpleComponent)

    # Manually build tree structure
    subject.items.append(
        Story(title="Primary", props={"name": "primary"}, parent=subject)
    )
    section.items["buttons"] = subject
    catalog.items["components"] = section

    layout = Layout(
        view_title="Test Page",
        site=catalog,
        children=html(t"<div>Test content</div>"),
        depth=0,
    )
    result = layout()

    # Verify result is not None
    assert result is not None

    # Get the aside element (sidebar)
    aside = get_by_tag_name(result, "aside")

    # Find all links in navigation
    links = query_all_by_tag_name(aside, "a")

    # Should have at least one link
    assert len(links) >= 1, "Navigation should have links"

    # All links should have href attributes
    for link in links:
        href = link.attrs.get("href")
        assert href, "All navigation links should have href attributes"
        assert href.startswith("/"), "Navigation links should start with /"


def test_navigation_tree_structure_supports_ancestor_traversal() -> None:
    """Test that navigation structure supports finding ancestor details elements."""
    catalog = Catalog(title="Test Catalog")
    section = Section(title="Components", name="components")
    subject = Subject(title="Buttons", name="buttons", target=SimpleComponent)

    # Manually build tree structure
    subject.items.append(Story(title="Primary", parent=subject))
    subject.items.append(Story(title="Secondary", parent=subject))
    section.items["buttons"] = subject
    catalog.items["components"] = section

    layout = Layout(
        view_title="Test Page",
        site=catalog,
        children=html(t"<div>Test content</div>"),
        depth=0,
        resource_path="components/buttons/story-1",
    )
    result = layout()

    # Verify result is not None
    assert result is not None

    # Get the aside element (sidebar)
    aside = get_by_tag_name(result, "aside")

    # Find all links in navigation
    links = query_all_by_tag_name(aside, "a")

    # Should have multiple links (one for each story)
    assert len(links) >= 2, "Navigation should have multiple story links"

    # Verify each link has an href that can be matched
    for link in links:
        href = link.attrs.get("href")
        assert href, "All navigation links should have href attributes"
        assert "/components/buttons/" in href, (
            "Links should contain section and subject"
        )

    # Find all details elements
    details_elements = query_all_by_tag_name(aside, "details")

    # Should have nested details (section -> subject)
    assert len(details_elements) >= 2, "Navigation should have nested structure"
