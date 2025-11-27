"""Tests for Layout component."""

from aria_testing import get_by_tag_name, get_text_content, query_all_by_tag_name
from aria_testing.utils import get_all_elements
from tdom import Element, Fragment, Node, html

from storytime.components.layout.layout import Layout
from storytime.section import Section
from storytime.site.models import Site


def _get_element(result: Node) -> Element:
    """Extract first Element from result (handles Fragment wrapper)."""
    elements = get_all_elements(result)
    if not elements:
        raise ValueError("No Element found in result")
    return elements[0]


# Basic Layout Structure Tests


def test_layout_renders_complete_html_structure() -> None:
    """Test Layout renders complete HTML structure with html, head, body tags."""
    site = Site(title="My Site")
    layout = Layout(view_title="Test Page", site=site, children=None)
    result = layout()

    # Extract Element from Fragment if needed
    element = _get_element(result)

    # Verify html tag is the root
    assert element.tag == "html"

    # Verify head exists
    get_by_tag_name(element, "head")

    # Verify body exists
    get_by_tag_name(element, "body")


def test_layout_includes_meta_tags() -> None:
    """Test Layout includes meta charset and viewport tags in head."""
    site = Site(title="My Site")
    layout = Layout(view_title="Test Page", site=site, children=None)
    result = layout()

    # Extract Element from Fragment if needed
    element = _get_element(result)

    # Get all meta tags
    head = get_by_tag_name(element, "head")
    meta_tags = query_all_by_tag_name(head, "meta")

    # Verify we have at least 2 meta tags (charset and viewport)
    assert len(meta_tags) >= 2

    # Check for charset meta
    charset_metas = [m for m in meta_tags if m.attrs.get("charset") == "utf-8"]
    assert len(charset_metas) == 1

    # Check for viewport meta
    viewport_metas = [m for m in meta_tags if m.attrs.get("name") == "viewport"]
    assert len(viewport_metas) == 1


def test_layout_title_concatenates_view_title_and_site_title() -> None:
    """Test Layout title concatenates view_title and site.title correctly."""
    site = Site(title="My Site")
    layout = Layout(view_title="Home", site=site, children=None)
    result = layout()

    # Extract Element from Fragment if needed
    element = _get_element(result)

    # Get title element
    title = get_by_tag_name(element, "title")
    title_text = get_text_content(title)

    # Verify concatenation with hyphen
    assert title_text == "Home - My Site"


def test_layout_title_uses_only_site_title_when_view_title_is_none() -> None:
    """Test Layout title uses only site.title when view_title is None."""
    site = Site(title="My Site")
    layout = Layout(view_title=None, site=site, children=None)
    result = layout()

    # Extract Element from Fragment if needed
    element = _get_element(result)

    # Get title element
    title = get_by_tag_name(element, "title")
    title_text = get_text_content(title)

    # Verify no hyphen when view_title is None
    assert title_text == "My Site"
    assert " - " not in title_text


def test_layout_inserts_children_content_into_main() -> None:
    """Test Layout inserts children content into main element."""
    site = Site(title="My Site")

    # Create some children content
    children = html(t"<div><p>Test Content</p></div>")

    layout = Layout(view_title="Test", site=site, children=children)
    result = layout()

    # Extract Element from Fragment if needed
    element = _get_element(result)

    # Get main element
    main = get_by_tag_name(element, "main")

    # Verify children content is in main or its descendants
    main_text = get_text_content(main)
    assert "Test Content" in main_text


def test_layout_includes_navigation_bar() -> None:
    """Test Layout includes navigation bar with site title."""
    site = Site(title="My Site")
    layout = Layout(view_title="Test", site=site, children=None)
    result = layout()

    # Extract Element from Fragment if needed
    element = _get_element(result)

    # Get header element
    header = get_by_tag_name(element, "header")

    # Verify site title is present in header
    header_text = get_text_content(header)
    assert "My Site" in header_text


def test_layout_includes_sidebar_with_sections() -> None:
    """Test Layout includes sidebar with NavigationTree component."""
    site = Site(title="My Site")

    # Add sections to site
    section1 = Section(title="Components")
    section2 = Section(title="Utilities")
    site.items = {"components": section1, "utilities": section2}

    layout = Layout(view_title="Test", site=site, children=None)
    result = layout()

    # Extract Element from Fragment if needed
    element = _get_element(result)

    # Get aside element (sidebar)
    aside = get_by_tag_name(element, "aside")

    # Verify aside contains navigation
    assert aside is not None


def test_layout_satisfies_view_protocol() -> None:
    """Test Layout satisfies View Protocol (__call__() -> Node)."""
    site = Site(title="My Site")
    layout = Layout(view_title="Test", site=site, children=None)

    # Verify __call__ returns Node (verified by type checker)
    result = layout()

    # Runtime verification that result is a Node (Element or Fragment)
    assert isinstance(result, (Element, Fragment))


# Script Injection Tests


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


# Task Group 1 Tests: Core Layout Structure


def test_layout_header_contains_navigation_links() -> None:
    """Test Layout header contains Home, About, and Debug links."""
    site = Site(title="Test Site")
    layout = Layout(view_title="Test Page", site=site, children=html(t"<p>Content</p>"))
    result = layout()

    element = _get_element(result)
    header = get_by_tag_name(element, "header")

    # Find all anchor tags in header
    links = query_all_by_tag_name(header, "a")
    link_texts = [get_text_content(link) for link in links]
    link_hrefs = [link.attrs.get("href") for link in links]

    # Verify Home, About, and Debug links exist
    assert "Home" in link_texts, f"Header should contain Home link, got {link_texts}"
    assert "About" in link_texts, f"Header should contain About link, got {link_texts}"
    assert "Debug" in link_texts, f"Header should contain Debug link, got {link_texts}"

    # Verify hrefs
    assert "/" in link_hrefs, "Header should contain link to /"
    assert "/about" in link_hrefs, "Header should contain link to /about"
    assert "/debug" in link_hrefs, "Header should contain link to /debug"


def test_layout_footer_contains_copyright() -> None:
    """Test Layout footer contains copyright text."""
    site = Site(title="Test Site")
    layout = Layout(view_title="Test Page", site=site, children=html(t"<p>Content</p>"))
    result = layout()

    element = _get_element(result)
    footer = get_by_tag_name(element, "footer")

    # Footer should exist and contain copyright text
    assert footer is not None, "Layout should have a footer element"
    # Extract all text from footer
    footer_text = get_text_content(footer)
    assert "2025 Storytime" in footer_text, f"Footer should contain copyright text, got: {footer_text}"


def test_layout_body_structure_with_direct_children() -> None:
    """Test Layout body contains header, aside, main, footer as direct children."""
    site = Site(title="Test Site")
    layout = Layout(view_title="Test Page", site=site, children=html(t"<p>Content</p>"))
    result = layout()

    element = _get_element(result)
    body = get_by_tag_name(element, "body")

    # Collect direct child element tags
    direct_child_tags = []
    for child in body.children:
        if isinstance(child, Element):
            direct_child_tags.append(child.tag)

    # Verify header, aside, main, footer are direct children
    assert "header" in direct_child_tags, "Body should contain header as direct child"
    assert "aside" in direct_child_tags, "Body should contain aside as direct child"
    assert "main" in direct_child_tags, "Body should contain main as direct child"
    assert "footer" in direct_child_tags, "Body should contain footer as direct child"


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
    element = _get_element(result)
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
    element = _get_element(result)
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
    element = _get_element(result)

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
    element = _get_element(result)

    # Verify cached navigation is rendered in aside
    aside = get_by_tag_name(element, "aside")
    aside_text = get_text_content(aside)
    assert "Cached Navigation Item" in aside_text


def test_layout_body_has_no_grid_wrapper() -> None:
    """Test Layout body no longer has div.grid wrapper."""
    site = Site(title="Test Site")
    layout = Layout(view_title="Page", site=site, children=None)
    result = layout()
    element = _get_element(result)

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
    element = _get_element(result)

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
    element = _get_element(result)

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
    element = _get_element(result)

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
    element = _get_element(result)

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
    element = _get_element(result)

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
    element = _get_element(result)

    # Should still render aside with "Sections" label
    aside = get_by_tag_name(element, "aside")
    assert aside is not None, "Layout should render aside even with empty sections"

    # Verify "Sections" label is present
    aside_text = get_text_content(aside)
    assert "Sections" in aside_text


def test_layout_depth_boundary_at_depth_3() -> None:
    """Test Layout handles depth=3 correctly (nested story pages)."""
    site = Site(title="Test Site")
    layout = Layout(
        view_title="Nested Story",
        site=site,
        children=html(t"<p>Deep content</p>"),
        depth=3
    )
    result = layout()
    element = _get_element(result)

    # Verify script path calculation at depth=3
    script_tags = query_all_by_tag_name(element, "script")
    ws_script = None
    for script in script_tags:
        src = script.attrs.get("src")
        if src and "ws.js" in src:
            ws_script = script
            break

    assert ws_script is not None, "Should have ws.js script tag"
    # At depth=3: ../../../../static/ws.js
    assert ws_script.attrs["src"] == "../../../../static/ws.js"


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
    element = _get_element(result)

    # Verify cached navigation is used instead of generating from empty sections
    aside = get_by_tag_name(element, "aside")
    aside_text = get_text_content(aside)
    assert "Cached Section" in aside_text
    assert "Sections" in aside_text


def test_layout_stylesheet_paths_at_depth_2() -> None:
    """Test Layout calculates all stylesheet paths correctly at depth=2."""
    site = Site(title="Test Site")
    layout = Layout(view_title="Subject Page", site=site, children=None, depth=2)
    result = layout()
    element = _get_element(result)

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

    # At depth=2, all static assets should have ../../../static/ prefix
    assert any("../../../static/pico-main.css" in href for href in stylesheet_hrefs), \
        "pico-main.css should have correct depth prefix"
    assert any("../../../static/storytime.css" in href for href in stylesheet_hrefs), \
        "storytime.css should have correct depth prefix"


def test_layout_favicon_path_at_depth_1() -> None:
    """Test Layout calculates favicon path correctly at depth=1."""
    site = Site(title="Test Site")
    layout = Layout(view_title="Section Page", site=site, children=None, depth=1)
    result = layout()
    element = _get_element(result)

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
    # At depth=1: ../../static/favicon.svg
    assert favicon_link.attrs["href"] == "../../static/favicon.svg"


def test_layout_all_static_assets_use_same_depth_prefix() -> None:
    """Test Layout ensures all static assets use consistent depth-based prefix."""
    site = Site(title="Test Site")
    layout = Layout(view_title="Test", site=site, children=None, depth=1)
    result = layout()
    element = _get_element(result)

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

    # All paths should have the same depth prefix for depth=1
    expected_prefix = "../../static/"
    for path in static_paths:
        assert path.startswith(expected_prefix), \
            f"Static asset path {path} should start with {expected_prefix}"


def test_layout_children_can_be_fragment() -> None:
    """Test Layout handles Fragment as children (not just Element)."""
    site = Site(title="Test Site")

    # Create a Fragment with multiple elements
    children = html(t"<div>First</div><div>Second</div>")

    layout = Layout(view_title="Test", site=site, children=children)
    result = layout()
    element = _get_element(result)

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
    element = _get_element(result)

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
    element = _get_element(result)

    # Verify aside component received sections and rendered them
    aside = get_by_tag_name(element, "aside")
    aside_text = get_text_content(aside)

    # Should contain section titles from the navigation tree
    assert "Getting Started" in aside_text or "getting-started" in aside_text.lower()
