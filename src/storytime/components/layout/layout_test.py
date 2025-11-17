"""Tests for Layout component."""

from aria_testing import get_by_tag_name, get_text_content, query_all_by_tag_name
from tdom import Element, Fragment, Node, Text, html

from storytime.components.layout.layout import Layout
from storytime.section import Section
from storytime.site.models import Site


def _get_element(result: Node) -> Element:
    """Extract Element from result (handles Fragment wrapper)."""
    if isinstance(result, Fragment):
        # Fragment contains the html element as first child
        for child in result.children:
            if isinstance(child, Element):
                return child
        raise ValueError("No Element found in Fragment")
    # Type guard - we know result is an Element if not Fragment
    if not isinstance(result, Element):
        raise ValueError("Result is not an Element or Fragment")
    return result


def _extract_text(node: Node) -> str:
    """Recursively extract text from a tdom node."""
    if isinstance(node, Text):
        return node.text
    if isinstance(node, str):
        return node
    if isinstance(node, Element):
        result = ""
        for child in node.children:
            result += _extract_text(child)
        return result
    return ""


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
    """Test Layout includes navigation bar with site branding."""
    site = Site(title="My Site")
    layout = Layout(view_title="Test", site=site, children=None)
    result = layout()

    # Extract Element from Fragment if needed
    element = _get_element(result)

    # Get header element
    header = get_by_tag_name(element, "header")

    # Verify "Storytime" branding is present in header
    header_text = get_text_content(header)
    assert "Storytime" in header_text


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
    link_texts = [_extract_text(link) for link in links]
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
    footer_text = _extract_text(footer)
    assert "2025 Storytime" in footer_text, f"Footer should contain copyright text, got: {footer_text}"


def test_layout_main_grid_structure() -> None:
    """Test Layout has correct grid structure with main.container > div.grid."""
    site = Site(title="Test Site")
    layout = Layout(view_title="Test Page", site=site, children=html(t"<p>Content</p>"))
    result = layout()

    element = _get_element(result)

    # Find main element
    main = get_by_tag_name(element, "main")
    assert main is not None, "Layout should have main element"
    assert main.attrs.get("class") == "container", "Main should have container class"

    # Find div.grid inside main
    grid_divs = [
        child
        for child in main.children
        if isinstance(child, Element) and child.tag == "div"
    ]
    assert len(grid_divs) > 0, "Main should contain div element"
    grid_div = grid_divs[0]
    assert grid_div.attrs.get("class") == "grid", "Div should have grid class"

    # Verify grid contains aside and article
    aside_found = False
    article_found = False
    for child in grid_div.children:
        if isinstance(child, Element):
            if child.tag == "aside":
                aside_found = True
            elif child.tag == "article":
                article_found = True

    assert aside_found, "Grid should contain aside element"
    assert article_found, "Grid should contain article element"


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
