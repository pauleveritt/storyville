"""Tests for seed command template content generation."""



from storyville import PACKAGE_DIR


def test_template_directory_exists():
    """Template directory should exist in package."""
    template_dir = PACKAGE_DIR / "templates" / "seed"
    assert template_dir.exists(), f"Template directory not found: {template_dir}"
    assert template_dir.is_dir(), "Template path should be a directory"


def test_root_stories_template_exists():
    """Root stories.py template should exist."""
    template_file = PACKAGE_DIR / "templates" / "seed" / "stories.py"
    assert template_file.exists(), "Root stories.py template not found"
    assert template_file.is_file(), "stories.py should be a file"


def test_themed_layout_template_exists():
    """ThemedLayout component template should exist in dedicated subdirectory."""
    themed_layout_file = (
        PACKAGE_DIR / "templates" / "seed" / "themed_layout" / "themed_layout.py"
    )
    assert themed_layout_file.exists(), "ThemedLayout template not found"
    assert themed_layout_file.is_file(), "themed_layout.py should be a file"


def test_component_templates_exist():
    """Component templates should exist for diverse component types."""
    components_dir = PACKAGE_DIR / "templates" / "seed" / "components"

    # Check that components directory exists
    assert components_dir.exists(), "Components directory not found"
    assert components_dir.is_dir(), "Components path should be a directory"

    # Check for specific component templates
    expected_components = ["button", "card", "form", "list_comp", "badge"]

    for component_name in expected_components:
        component_file = components_dir / f"{component_name}.py"
        assert component_file.exists(), f"Component template not found: {component_name}.py"


def test_root_stories_template_has_valid_python():
    """Root stories.py template should contain valid Python code."""
    template_file = PACKAGE_DIR / "templates" / "seed" / "stories.py"

    # Read the template
    content = template_file.read_text()

    # Verify it imports Catalog
    assert "from storyville import Catalog" in content or "from storyville.catalog import Catalog" in content

    # Verify it defines this_catalog function
    assert "def this_catalog()" in content

    # Verify it has themed_layout parameter
    assert "themed_layout" in content


def test_themed_layout_template_has_valid_structure():
    """ThemedLayout template should have dataclass structure with __call__ method."""
    template_file = (
        PACKAGE_DIR / "templates" / "seed" / "themed_layout" / "themed_layout.py"
    )

    content = template_file.read_text()

    # Should be a dataclass
    assert "@dataclass" in content

    # Should have story_title and children parameters
    assert "story_title" in content
    assert "children" in content

    # Should have __call__ method
    assert "def __call__" in content

    # Should use tdom
    assert "from tdom import" in content


def test_component_templates_have_assertions():
    """Component templates should include sample assertion functions."""
    components_dir = PACKAGE_DIR / "templates" / "seed" / "components"
    button_file = components_dir / "button.py"

    content = button_file.read_text()

    # Should have assertion function(s)
    # Looking for common assertion patterns
    assert "def check_" in content or "def assert_" in content or "def test_" in content

    # Should have assertion logic
    assert "assert" in content
