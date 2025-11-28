"""Tests for Layout component."""

from aria_testing import get_by_tag_name, get_text_content, query_all_by_tag_name
from tdom import html, Element

from storytime.components.layout.layout import Layout
from storytime.section import Section
from storytime.site.models import Site

def test_layout_accepts_current_path_parameter() -> None:
    """Test Layout accepts current_path parameter."""
    site = Site(title="Test Site")
    # Should not raise error with current_path parameter
    layout = Layout(
        view_title="Test Page",
        site=site,
        children=html(t"<p>Content</p>"),
        current_path="section/subject/story",
    )
    result = layout()
    element = result
    assert element is not None, "Layout should render with current_path parameter"

def test_layout_current_path_can_be_none() -> None:
    """Test Layout current_path can be None."""
    site = Site(title="Test Site")
    # Should work with current_path=None
    layout = Layout(
        view_title="Test Page",
        site=site,
        children=html(t"<p>Content</p>"),
        current_path=None,
    )
    result = layout()
    element = result
    assert element is not None, "Layout should render with current_path=None"

# Component Composition Tests

def test_layout_renders_all_four_components() -> None:
    """Test Layout renders header, aside, main, and footer components."""
    site = Site(title="Test Site")
    section = Section(title="Test Section")
    site.items = {"test": section}

    layout = Layout(
        view_title="Test Page",
        site=site,
        children=html(t"<p>Content</p>"),
        current_path="test/page",
    )
    result = layout()
    element = result

    # Verify all four components are rendered
    body = get_by_tag_name(element, "body")

    # Check for header
    header = get_by_tag_name(body, "header")
    assert header is not None, "Layout should render LayoutHeader component"

    # Check for aside
    aside = get_by_tag_name(body, "aside")
    assert aside is not None, "Layout should render LayoutAside component"

    # Check for main
    main = get_by_tag_name(body, "main")
    assert main is not None, "Layout should render LayoutMain component"

    # Check for footer
    footer = get_by_tag_name(body, "footer")
    assert footer is not None, "Layout should render LayoutFooter component"

def test_layout_passes_cached_navigation_to_aside() -> None:
    """Test Layout passes cached_navigation HTML to LayoutAside."""
    site = Site(title="Test Site")
    cached_nav = "<nav><ul><li>Cached Navigation Item</li></ul></nav>"

    layout = Layout(
        view_title="Page",
        site=site,
        children=None,
        cached_navigation=cached_nav,
    )
    result = layout()
    element = result

    # Verify cached navigation is rendered in aside
    aside = get_by_tag_name(element, "aside")
    aside_text = get_text_content(aside)
    assert "Cached Navigation Item" in aside_text

def test_layout_body_has_no_grid_wrapper() -> None:
    """Test Layout body no longer has div.grid wrapper."""
    site = Site(title="Test Site")
    layout = Layout(view_title="Page", site=site, children=None)
    result = layout()
    element = result

    body = get_by_tag_name(element, "body")

    # Check that there is no div.grid as direct child of body
    for child in body.children:
        if isinstance(child, Element) and child.tag == "div":
            class_attr = child.attrs.get("class") or ""
            assert "grid" not in class_attr, "Body should NOT contain div.grid wrapper"

# CSS Grid Implementation Tests

def test_layout_body_contains_four_direct_child_elements() -> None:
    """Test Layout body has exactly four direct child elements: header, aside, main, footer."""
    site = Site(title="Test Site")
    layout = Layout(view_title="Page", site=site, children=html(t"<p>Content</p>"))
    result = layout()
    element = result

    body = get_by_tag_name(element, "body")

    # Collect all direct child elements
    direct_children = [child for child in body.children if isinstance(child, Element)]

    # Should have exactly 4 direct child elements
    assert len(direct_children) == 4, f"Body should have 4 direct child elements, got {len(direct_children)}"

    # Verify the tags are correct
    child_tags = [child.tag for child in direct_children]
    assert child_tags == ["header", "aside", "main", "footer"], \
        f"Body children should be [header, aside, main, footer], got {child_tags}"

def test_layout_header_is_first_child_of_body() -> None:
    """Test Layout header element is the first direct child of body."""
    site = Site(title="Test Site")
    layout = Layout(view_title="Page", site=site, children=None)
    result = layout()
    element = result

    body = get_by_tag_name(element, "body")

    # Get first element child
    first_element = None
    for child in body.children:
        if isinstance(child, Element):
            first_element = child
            break

    assert first_element is not None, "Body should have at least one element child"
    assert first_element.tag == "header", f"First child of body should be header, got {first_element.tag}"

def test_layout_footer_is_last_child_of_body() -> None:
    """Test Layout footer element is the last direct child of body."""
    site = Site(title="Test Site")
    layout = Layout(view_title="Page", site=site, children=None)
    result = layout()
    element = result

    body = get_by_tag_name(element, "body")

    # Get all element children
    element_children = [child for child in body.children if isinstance(child, Element)]

    assert len(element_children) > 0, "Body should have element children"
    last_element = element_children[-1]
    assert last_element.tag == "footer", f"Last child of body should be footer, got {last_element.tag}"

def test_layout_aside_and_main_are_middle_children() -> None:
    """Test Layout aside and main elements are positioned between header and footer."""
    site = Site(title="Test Site")
    layout = Layout(view_title="Page", site=site, children=html(t"<p>Content</p>"))
    result = layout()
    element = result

    body = get_by_tag_name(element, "body")

    # Get all element children in order
    element_children = [child for child in body.children if isinstance(child, Element)]
    child_tags = [child.tag for child in element_children]

    # Verify order: header, aside, main, footer
    assert len(child_tags) == 4, f"Should have 4 children, got {len(child_tags)}"
    assert child_tags[0] == "header", "First child should be header"
    assert child_tags[1] == "aside", "Second child should be aside"
    assert child_tags[2] == "main", "Third child should be main"
    assert child_tags[3] == "footer", "Fourth child should be footer"

def test_layout_aside_appears_before_main() -> None:
    """Test Layout aside element appears before main element in DOM order."""
    site = Site(title="Test Site")
    section = Section(title="Test Section")
    site.items = {"test": section}

    layout = Layout(view_title="Page", site=site, children=html(t"<p>Content</p>"))
    result = layout()
    element = result

    body = get_by_tag_name(element, "body")

    # Find aside and main elements
    aside_index = None
    main_index = None

    for i, child in enumerate(body.children):
        if isinstance(child, Element):
            if child.tag == "aside":
                aside_index = i
            elif child.tag == "main":
                main_index = i

    assert aside_index is not None, "Body should contain aside element"
    assert main_index is not None, "Body should contain main element"
    assert aside_index < main_index, "Aside should appear before main in DOM order"

# Task Group 4: Strategic Edge Case Tests

def test_layout_with_empty_sections_dict() -> None:
    """Test Layout renders correctly when site has no sections (empty dict)."""
    site = Site(title="Test Site")
    site.items = {}  # Empty sections dict

    layout = Layout(view_title="Page", site=site, children=html(t"<p>Content</p>"))
    result = layout()
    element = result

    # Should still render aside with "Sections" label
    aside = get_by_tag_name(element, "aside")
    assert aside is not None, "Layout should render aside even with empty sections"

    # Verify "Sections" label is present
    aside_text = get_text_content(aside)
    assert "Sections" in aside_text

def test_layout_depth_boundary_at_depth_3() -> None:
    """Test Layout adds correct depth prefix at depth=3."""
    site = Site(title="Test Site")
    layout = Layout(
        view_title="Nested Story",
        site=site,
        children=html(t"<p>Deep content</p>"),
        depth=3
    )
    result = layout()
    element = result

    # Verify script path has correct depth prefix
    script_tags = query_all_by_tag_name(element, "script")
    ws_script = None
    for script in script_tags:
        src = script.attrs.get("src")
        if src and "ws.js" in src:
            ws_script = script
            break

    assert ws_script is not None, "Should have ws.js script tag"
    # depth=3 means 3 directories deep = ../../../static/ws.js
    assert ws_script.attrs["src"] == "../../../static/ws.js"

def test_layout_cached_navigation_with_empty_sections() -> None:
    """Test Layout with cached_navigation and empty sections dict."""
    site = Site(title="Test Site")
    site.items = {}
    cached_nav = "<nav><ul><li>Cached Section</li></ul></nav>"

    layout = Layout(
        view_title="Page",
        site=site,
        children=None,
        cached_navigation=cached_nav,
    )
    result = layout()
    element = result

    # Verify cached navigation is used instead of generating from empty sections
    aside = get_by_tag_name(element, "aside")
    aside_text = get_text_content(aside)
    assert "Cached Section" in aside_text
    assert "Sections" in aside_text

def test_layout_stylesheet_paths_at_depth_2() -> None:
    """Test Layout calculates stylesheet paths with correct depth prefix."""
    site = Site(title="Test Site")
    layout = Layout(view_title="Subject Page", site=site, children=None, depth=2)
    result = layout()
    element = result

    head = get_by_tag_name(element, "head")
    link_tags = query_all_by_tag_name(head, "link")

    # Find stylesheet links
    stylesheet_hrefs = []
    for link in link_tags:
        rel = link.attrs.get("rel")
        if rel == "stylesheet":
            href = link.attrs.get("href")
            if href:
                stylesheet_hrefs.append(href)

    # depth=2 means 2 directories deep = ../../static/
    assert any("../../static/pico-main.css" in href for href in stylesheet_hrefs), \
        "pico-main.css should have correct depth prefix"
    assert any("../../static/storytime.css" in href for href in stylesheet_hrefs), \
        "storytime.css should have correct depth prefix"

def test_layout_favicon_path_at_depth_1() -> None:
    """Test Layout calculates favicon path with correct depth prefix."""
    site = Site(title="Test Site")
    layout = Layout(view_title="Section Page", site=site, children=None, depth=1)
    result = layout()
    element = result

    head = get_by_tag_name(element, "head")
    link_tags = query_all_by_tag_name(head, "link")

    # Find favicon link
    favicon_link = None
    for link in link_tags:
        rel = link.attrs.get("rel")
        if rel == "icon":
            favicon_link = link
            break

    assert favicon_link is not None, "Should have favicon link"
    # depth=1 means 1 directory deep, so ../static/favicon.svg
    assert favicon_link.attrs["href"] == "../static/favicon.svg"

def test_layout_all_static_assets_use_same_depth_prefix() -> None:
    """Test Layout uses consistent depth prefix for all static assets."""
    site = Site(title="Test Site")
    layout = Layout(view_title="Test", site=site, children=None, depth=1)
    result = layout()
    element = result

    head = get_by_tag_name(element, "head")

    # Collect all static asset paths
    link_tags = query_all_by_tag_name(head, "link")
    script_tags = query_all_by_tag_name(head, "script")

    static_paths = []
    for link in link_tags:
        href = link.attrs.get("href")
        if href and "static/" in href:
            static_paths.append(href)

    for script in script_tags:
        src = script.attrs.get("src")
        if src and "static/" in src:
            static_paths.append(src)

    # All paths should use the same depth prefix (depth=1 means 1 dir deep = ../static/)
    expected_prefix = "../static/"
    for path in static_paths:
        assert path.startswith(expected_prefix), \
            f"Static asset path {path} should start with {expected_prefix}"

def test_layout_children_can_be_fragment() -> None:
    """Test Layout handles  as children (not just )."""
    site = Site(title="Test Site")

    # Create a  with multiple elements
    children = html(t"<div>First</div><div>Second</div>")

    layout = Layout(view_title="Test", site=site, children=children)
    result = layout()
    element = result

    # Verify both pieces of content are rendered in main
    main = get_by_tag_name(element, "main")
    main_text = get_text_content(main)
    assert "First" in main_text
    assert "Second" in main_text

def test_layout_depth_affects_header_navigation_links() -> None:
    """Test Layout passes depth to LayoutHeader for correct navigation link paths."""
    site = Site(title="Test Site")
    layout = Layout(view_title="Page", site=site, children=None, depth=1)
    result = layout()
    element = result

    # The header should have been instantiated with depth=1
    # This test verifies the integration between Layout and LayoutHeader
    header = get_by_tag_name(element, "header")
    assert header is not None

    # Verify header contains navigation links (integration check)
    links = query_all_by_tag_name(header, "a")
    assert len(links) >= 3, "Header should contain navigation links"

def test_layout_passes_site_items_to_aside() -> None:
    """Test Layout passes site.items dict to LayoutAside component."""
    site = Site(title="Test Site")
    section1 = Section(title="Getting Started")
    section2 = Section(title="Advanced")
    site.items = {"getting-started": section1, "advanced": section2}

    layout = Layout(view_title="Page", site=site, children=None, current_path="getting-started/intro")
    result = layout()
    element = result

    # Verify aside component received sections and rendered them
    aside = get_by_tag_name(element, "aside")
    aside_text = get_text_content(aside)

    # Should contain section titles from the navigation tree
    assert "Getting Started" in aside_text or "getting-started" in aside_text.lower()
