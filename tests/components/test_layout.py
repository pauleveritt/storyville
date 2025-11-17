"""Test the Layout component rendering and script injection."""

from aria_testing import get_by_tag_name, query_all_by_tag_name
from tdom import Element, Fragment, Node, html

from storytime.components.layout.layout import Layout
from storytime.site.models import Site


def _get_element(result: Node) -> Element:
    """Extract Element from result (handles Fragment wrapper)."""
    if isinstance(result, Fragment):
        # Fragment contains the html element as first child
        for child in result.children:
            if isinstance(child, Element):
                return child
        raise ValueError("No Element found in Fragment")
    # Type guard assertion - we know result is an Element if not Fragment
    assert isinstance(result, Element)
    return result


def test_layout_includes_script_tag() -> None:
    """Test Layout includes script tag in rendered HTML."""
    site = Site(title="Test Site")
    layout = Layout(view_title="Test Page", site=site, children=html(t"<p>Content</p>"))
    result = layout()

    # Extract Element from result
    element = _get_element(result)

    # Verify script tag exists
    script_tags = query_all_by_tag_name(element, "script")
    assert len(script_tags) > 0, "Layout should include at least one script tag"


def test_layout_script_tag_references_ws_js() -> None:
    """Test Layout script tag references /static/ws.js."""
    site = Site(title="Test Site")
    layout = Layout(view_title="Test Page", site=site, children=html(t"<p>Content</p>"))
    result = layout()

    # Extract Element from result
    element = _get_element(result)

    # Find script tag with src attribute
    script_tags = query_all_by_tag_name(element, "script")
    ws_script = None
    for script in script_tags:
        src = script.attrs.get("src")
        if src and "ws.js" in src:
            ws_script = script
            break

    assert ws_script is not None, "Should have script tag referencing ws.js"
    # The src should reference /static/ws.js with proper depth prefix
    src_attr = ws_script.attrs.get("src")
    assert src_attr is not None, "ws.js script should have src attribute"
    assert "static/ws.js" in src_attr, f"Script src should reference static/ws.js, got: {src_attr}"


def test_layout_script_in_head() -> None:
    """Test Layout script tag appears in head section."""
    site = Site(title="Test Site")
    layout = Layout(view_title="Test Page", site=site, children=html(t"<p>Content</p>"))
    result = layout()

    # Extract Element from result
    element = _get_element(result)

    # Get head element
    head = get_by_tag_name(element, "head")

    # Verify head has children (script should be among them)
    assert head.children, "Head should have children"

    # Find script tag in head by checking all children
    script_found = False
    for child in head.children:
        if isinstance(child, Element) and child.tag == "script":
            # Check if it's the ws.js script
            src = child.attrs.get("src")
            if src and "ws.js" in src:
                script_found = True
                break

    assert script_found, "Script tag should be in head element"


def test_layout_script_works_at_depth_0() -> None:
    """Test Layout script src path is correct at depth=0 (site root)."""
    site = Site(title="Test Site")
    layout = Layout(
        view_title="Test Page", site=site, children=html(t"<p>Content</p>"), depth=0
    )
    result = layout()

    # Extract Element from result
    element = _get_element(result)

    # Find ws.js script
    script_tags = query_all_by_tag_name(element, "script")
    ws_script = None
    for script in script_tags:
        src = script.attrs.get("src")
        if src and "ws.js" in src:
            ws_script = script
            break

    assert ws_script is not None, "Should have ws.js script tag"
    # At depth=0: ../static/ws.js
    assert ws_script.attrs["src"] == "../static/ws.js"


def test_layout_script_works_at_depth_1() -> None:
    """Test Layout script src path is correct at depth=1 (section pages)."""
    site = Site(title="Test Site")
    layout = Layout(
        view_title="Test Page", site=site, children=html(t"<p>Content</p>"), depth=1
    )
    result = layout()

    # Extract Element from result
    element = _get_element(result)

    # Find ws.js script
    script_tags = query_all_by_tag_name(element, "script")
    ws_script = None
    for script in script_tags:
        src = script.attrs.get("src")
        if src and "ws.js" in src:
            ws_script = script
            break

    assert ws_script is not None, "Should have ws.js script tag"
    # At depth=1: ../../static/ws.js
    assert ws_script.attrs["src"] == "../../static/ws.js"


def test_layout_script_works_at_depth_2() -> None:
    """Test Layout script src path is correct at depth=2 (subject pages)."""
    site = Site(title="Test Site")
    layout = Layout(
        view_title="Test Page", site=site, children=html(t"<p>Content</p>"), depth=2
    )
    result = layout()

    # Extract Element from result
    element = _get_element(result)

    # Find ws.js script
    script_tags = query_all_by_tag_name(element, "script")
    ws_script = None
    for script in script_tags:
        src = script.attrs.get("src")
        if src and "ws.js" in src:
            ws_script = script
            break

    assert ws_script is not None, "Should have ws.js script tag"
    # At depth=2: ../../../static/ws.js
    assert ws_script.attrs["src"] == "../../../static/ws.js"
