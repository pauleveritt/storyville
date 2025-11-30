"""Tests for BaseNode resource_path functionality."""


from storytime.catalog import Catalog
from storytime.section import Section
from storytime.subject import Subject


def test_base_node_resource_path_initialization():
    """Test that resource_path is initialized with empty string default."""
    catalog = Catalog(title="Test Catalog")
    assert hasattr(catalog, "resource_path")
    assert catalog.resource_path == ""


def test_catalog_resource_path_after_post_update(mock_tree_node):
    """Test that Catalog resource_path remains empty string after post_update."""
    catalog = Catalog(title="Test Catalog")
    tree_node = mock_tree_node(name="", package_location=".")

    catalog.post_update(parent=None, tree_node=tree_node)

    assert catalog.resource_path == ""
    assert catalog.name == ""


def test_section_resource_path_after_post_update(mock_tree_node):
    """Test that Section resource_path is set to section name."""
    catalog = Catalog(title="Test Catalog")
    catalog_node = mock_tree_node(name="", package_location=".")
    catalog.post_update(parent=None, tree_node=catalog_node)

    section = Section(title="Components")
    section_node = mock_tree_node(name="components", package_location=".components")

    section.post_update(parent=catalog, tree_node=section_node)

    assert section.resource_path == "components"
    assert section.name == "components"


def test_subject_resource_path_after_post_update(mock_tree_node):
    """Test that Subject resource_path includes parent section path."""
    catalog = Catalog(title="Test Catalog")
    catalog_node = mock_tree_node(name="", package_location=".")
    catalog.post_update(parent=None, tree_node=catalog_node)

    section = Section(title="Components")
    section_node = mock_tree_node(name="components", package_location=".components")
    section.post_update(parent=catalog, tree_node=section_node)

    subject = Subject(title="Button")
    subject_node = mock_tree_node(name="button", package_location=".components.button")

    subject.post_update(parent=section, tree_node=subject_node)

    assert subject.resource_path == "components/button"
    assert subject.name == "button"


def test_nested_resource_path_format(mock_tree_node):
    """Test resource_path format for deeply nested structure."""
    catalog = Catalog(title="Test Catalog")
    catalog_node = mock_tree_node(name="", package_location=".")
    catalog.post_update(parent=None, tree_node=catalog_node)

    section = Section(title="UI Components")
    section_node = mock_tree_node(name="ui-components", package_location=".ui-components")
    section.post_update(parent=catalog, tree_node=section_node)

    subject = Subject(title="Form Elements")
    subject_node = mock_tree_node(name="form-elements", package_location=".ui-components.form-elements")
    subject.post_update(parent=section, tree_node=subject_node)

    # Verify the full path
    assert catalog.resource_path == ""
    assert section.resource_path == "ui-components"
    assert subject.resource_path == "ui-components/form-elements"


def test_resource_path_inheritance_across_types(mock_tree_node):
    """Test that resource_path flows correctly through Catalog/Section/Subject hierarchy."""
    # Create the hierarchy
    catalog = Catalog(title="Test Catalog")
    catalog_node = mock_tree_node(name="", package_location=".")
    catalog.post_update(parent=None, tree_node=catalog_node)

    # Add section
    section1 = Section(title="Section 1")
    section1_node = mock_tree_node(name="section1", package_location=".section1")
    section1.post_update(parent=catalog, tree_node=section1_node)
    catalog.items["section1"] = section1

    # Add another section
    section2 = Section(title="Section 2")
    section2_node = mock_tree_node(name="section2", package_location=".section2")
    section2.post_update(parent=catalog, tree_node=section2_node)
    catalog.items["section2"] = section2

    # Add subjects under section1
    subject1 = Subject(title="Subject 1A")
    subject1_node = mock_tree_node(name="subject1a", package_location=".section1.subject1a")
    subject1.post_update(parent=section1, tree_node=subject1_node)
    section1.items["subject1a"] = subject1

    subject2 = Subject(title="Subject 1B")
    subject2_node = mock_tree_node(name="subject1b", package_location=".section1.subject1b")
    subject2.post_update(parent=section1, tree_node=subject2_node)
    section1.items["subject1b"] = subject2

    # Verify all paths
    assert catalog.resource_path == ""
    assert section1.resource_path == "section1"
    assert section2.resource_path == "section2"
    assert subject1.resource_path == "section1/subject1a"
    assert subject2.resource_path == "section1/subject1b"


def test_resource_path_type_is_str(mock_tree_node):
    """Test that resource_path is typed as str (non-optional)."""
    catalog = Catalog(title="Test Catalog")

    # Should have resource_path as str, not None
    assert isinstance(catalog.resource_path, str)
    assert catalog.resource_path is not None

    # After post_update, should still be str
    catalog_node = mock_tree_node(name="", package_location=".")
    catalog.post_update(parent=None, tree_node=catalog_node)

    assert isinstance(catalog.resource_path, str)
    assert catalog.resource_path is not None
