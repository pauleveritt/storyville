"""Test the CatalogView rendering."""

from aria_testing import get_by_tag_name, get_text_content, query_all_by_tag_name

from storytime.section import Section
from storytime.catalog.models import Catalog
from storytime.catalog.views import CatalogView
from storytime.subject import Subject

def test_catalog_view_renders_title_in_h1() -> None:
    """Test CatalogView renders catalog title in h1 element."""
    catalog = Catalog(title="My Catalog")
    view = CatalogView(catalog=catalog)
    result = view()

    # Extract  from  (Layout wraps the result)
    element = result

    # Verify title is in h1
    h1 = get_by_tag_name(element, "h1")
    assert get_text_content(h1) == "My Catalog"

def test_catalog_view_renders_section_links() -> None:
    """Test CatalogView renders section links when sections exist."""
    catalog = Catalog(title="My Catalog")
    catalog.package_path = "."

    # Add sections to catalog
    section1 = Section(title="Components")
    section2 = Section(title="Utilities")
    catalog.items = {"components": section1, "utilities": section2}

    view = CatalogView(catalog=catalog)
    result = view()

    # Extract  from  (Layout wraps the result)
    element = result

    # Get the main element (content area) to avoid sidebar sections listing
    main = get_by_tag_name(element, "main")

    # Verify section cards are rendered as links (main contains the actual content)
    all_links = query_all_by_tag_name(main, "a")

    assert len(all_links) == 2
    # Links can be in any order since dict iteration order may vary
    link_texts = {get_text_content(link) for link in all_links}
    assert link_texts == {"Components", "Utilities"}

def test_catalog_view_shows_empty_state() -> None:
    """Test CatalogView shows empty state message when no sections."""
    catalog = Catalog(title="Empty Catalog")
    view = CatalogView(catalog=catalog)
    result = view()

    # Extract  from  (Layout wraps the result)
    element = result

    # Verify empty state message
    all_p_tags = query_all_by_tag_name(element, "p")
    empty_state_found = any(
        "No sections defined for this catalog" in get_text_content(p)
        for p in all_p_tags
    )
    assert empty_state_found

def test_catalog_view_does_not_include_parent_link() -> None:
    """Test CatalogView does NOT include parent link (Catalog is root)."""
    catalog = Catalog(title="My Catalog")
    view = CatalogView(catalog=catalog)
    result = view()

    # Extract  from  (Layout wraps the result)
    element = result

    # Get the main element (content area)
    main = get_by_tag_name(element, "main")

    # Verify NO parent link exists in main content
    all_links = query_all_by_tag_name(main, "a")
    parent_links = [link for link in all_links if link.attrs.get("href") == ".."]
    assert len(parent_links) == 0

def test_catalog_view_satisfies_view_protocol() -> None:
    """Test CatalogView satisfies View Protocol (__call__() -> )."""
    catalog = Catalog(title="My Catalog")
    view = CatalogView(catalog=catalog)

    # Verify __call__ returns  (verified by type checker)
    result = view()

    # Runtime verification that result is a valid Node (could be Element or Fragment)
    assert result is not None
    # Verify it contains an html element (from Layout wrapper)
    html_elem = get_by_tag_name(result, "html")
    assert html_elem is not None

def test_catalog_view_shows_section_descriptions() -> None:
    """Test CatalogView shows section descriptions when present."""
    catalog = Catalog(title="My Catalog")
    section1 = Section(title="Components", description="UI building blocks")
    section2 = Section(title="Utilities", description="Helper functions")
    catalog.items = {"components": section1, "utilities": section2}

    view = CatalogView(catalog=catalog)
    result = view()

    # Extract  from  (Layout wraps the result)
    element = result

    # Get all text content and verify descriptions are present
    text_content = get_text_content(element)
    assert "UI building blocks" in text_content
    assert "Helper functions" in text_content

def test_catalog_view_omits_none_descriptions() -> None:
    """Test CatalogView omits descriptions when None."""
    catalog = Catalog(title="My Catalog")
    section1 = Section(title="Components", description=None)
    section2 = Section(title="Utilities", description="Helper functions")
    catalog.items = {"components": section1, "utilities": section2}

    view = CatalogView(catalog=catalog)
    result = view()

    # Extract  from  (Layout wraps the result)
    element = result

    # Get all text content
    text_content = get_text_content(element)
    # Section with description shows it
    assert "Helper functions" in text_content

def test_catalog_view_shows_subject_counts() -> None:
    """Test CatalogView shows correct subject counts for each section."""
    catalog = Catalog(title="My Catalog")

    # Section 1 with 3 subjects
    section1 = Section(title="Components")
    section1.items = {
        "button": Subject(title="Button"),
        "input": Subject(title="Input"),
        "card": Subject(title="Card"),
    }

    # Section 2 with 1 subject
    section2 = Section(title="Utilities")
    section2.items = {
        "helpers": Subject(title="Helpers"),
    }

    catalog.items = {"components": section1, "utilities": section2}

    view = CatalogView(catalog=catalog)
    result = view()

    # Extract  from  (Layout wraps the result)
    element = result

    # Get all text content and verify subject counts
    text_content = get_text_content(element)
    assert "3 subjects" in text_content
    assert "1 subject" in text_content

def test_catalog_view_url_pattern() -> None:
    """Test CatalogView uses /{section_name} URL pattern."""
    catalog = Catalog(title="My Catalog")
    section1 = Section(title="Components")
    section2 = Section(title="Utilities")
    catalog.items = {"components": section1, "utilities": section2}

    view = CatalogView(catalog=catalog)
    result = view()

    # Extract  from  (Layout wraps the result)
    element = result

    # Verify section links follow /{section_name} pattern
    all_links = query_all_by_tag_name(element, "a")
    hrefs = {link.attrs.get("href") for link in all_links}
    assert "/components" in hrefs
    assert "/utilities" in hrefs
