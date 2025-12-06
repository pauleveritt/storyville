"""Tests for seed catalog generation engine."""

import shutil
from pathlib import Path

import pytest

from storytime.__main__ import SizeConfig, seed


@pytest.fixture
def temp_output_dir(tmp_path: Path) -> Path:
    """Provide a temporary output directory for testing.

    Args:
        tmp_path: Pytest temporary path fixture.

    Yields:
        Path to temporary directory for catalog output.
    """
    output_dir = tmp_path / "test_catalog"
    yield output_dir
    # Cleanup
    if output_dir.exists():
        shutil.rmtree(output_dir)


def test_small_catalog_structure(temp_output_dir: Path) -> None:
    """Test that small catalog generates correct directory structure.

    Small catalog should have:
    - 1 section directory
    - 2 subjects within that section
    - Root stories.py and themed_layout subdirectory
    """
    from storytime.__main__ import generate_catalog

    config = SizeConfig(sections=1, subjects=2, stories_per_subject=2)
    generate_catalog(temp_output_dir, config)

    # Check root files exist
    assert (temp_output_dir / "stories.py").exists()
    assert (temp_output_dir / "__init__.py").exists()

    # Check themed_layout subdirectory exists
    assert (temp_output_dir / "themed_layout").is_dir()
    assert (temp_output_dir / "themed_layout" / "themed_layout.py").exists()
    assert (temp_output_dir / "themed_layout" / "__init__.py").exists()

    # Check that we have 1 section directory
    section_dirs = [d for d in temp_output_dir.iterdir() if d.is_dir() and d.name.startswith("section_")]
    assert len(section_dirs) == 1

    # Check section has __init__.py
    section = section_dirs[0]
    assert (section / "__init__.py").exists()

    # Check that section has 2 subject directories
    subject_dirs = [d for d in section.iterdir() if d.is_dir()]
    assert len(subject_dirs) == 2


def test_section_subject_story_hierarchy(temp_output_dir: Path) -> None:
    """Test that section/subject/story hierarchy matches configuration.

    Medium catalog should have:
    - 2 sections
    - 4 subjects total distributed across sections
    - Each subject has stories.py and component file
    """
    from storytime.__main__ import generate_catalog

    config = SizeConfig(sections=2, subjects=4, stories_per_subject=2)
    generate_catalog(temp_output_dir, config)

    # Count section directories
    section_dirs = [d for d in temp_output_dir.iterdir() if d.is_dir() and d.name.startswith("section_")]
    assert len(section_dirs) == 2

    # Count total subjects across all sections
    total_subjects = 0
    for section in section_dirs:
        subject_dirs = [d for d in section.iterdir() if d.is_dir()]
        total_subjects += len(subject_dirs)

        # Verify each subject has required files
        for subject_dir in subject_dirs:
            assert (subject_dir / "__init__.py").exists()
            assert (subject_dir / "stories.py").exists()
            # Should have exactly one component python file (besides __init__.py and stories.py)
            py_files = [f for f in subject_dir.glob("*.py") if f.name not in ("__init__.py", "stories.py")]
            assert len(py_files) == 1

    assert total_subjects == 4


def test_all_init_files_created(temp_output_dir: Path) -> None:
    """Test that all __init__.py files are created throughout the hierarchy."""
    from storytime.__main__ import generate_catalog

    config = SizeConfig(sections=2, subjects=4, stories_per_subject=2)
    generate_catalog(temp_output_dir, config)

    # Root __init__.py
    assert (temp_output_dir / "__init__.py").exists()

    # ThemedLayout __init__.py
    assert (temp_output_dir / "themed_layout" / "__init__.py").exists()

    # All section __init__.py files
    section_dirs = [d for d in temp_output_dir.iterdir() if d.is_dir() and d.name.startswith("section_")]
    for section in section_dirs:
        assert (section / "__init__.py").exists()

        # All subject __init__.py files
        subject_dirs = [d for d in section.iterdir() if d.is_dir()]
        for subject in subject_dirs:
            assert (subject / "__init__.py").exists()


def test_themed_layout_component_copied(temp_output_dir: Path) -> None:
    """Test that ThemedLayout component is copied to correct location."""
    from storytime.__main__ import generate_catalog

    config = SizeConfig(sections=1, subjects=2, stories_per_subject=2)
    generate_catalog(temp_output_dir, config)

    themed_layout_dir = temp_output_dir / "themed_layout"
    assert themed_layout_dir.is_dir()
    assert (themed_layout_dir / "themed_layout.py").exists()
    assert (themed_layout_dir / "__init__.py").exists()

    # Verify the content has the ThemedLayout class
    content = (themed_layout_dir / "themed_layout.py").read_text()
    assert "class ThemedLayout" in content
    assert "def __call__(self)" in content


def test_root_stories_file_generated(temp_output_dir: Path) -> None:
    """Test that root stories.py file is created with Catalog definition."""
    from storytime.__main__ import generate_catalog

    config = SizeConfig(sections=1, subjects=2, stories_per_subject=2)
    generate_catalog(temp_output_dir, config)

    stories_file = temp_output_dir / "stories.py"
    assert stories_file.exists()

    content = stories_file.read_text()
    assert "from storytime import Catalog" in content
    assert "def this_catalog()" in content
    assert "themed_layout_wrapper" in content


def test_component_files_in_subjects(temp_output_dir: Path) -> None:
    """Test that component files are generated in subject directories."""
    from storytime.__main__ import generate_catalog

    config = SizeConfig(sections=1, subjects=2, stories_per_subject=2)
    generate_catalog(temp_output_dir, config)

    section_dirs = [d for d in temp_output_dir.iterdir() if d.is_dir() and d.name.startswith("section_")]
    section = section_dirs[0]

    subject_dirs = [d for d in section.iterdir() if d.is_dir()]

    for subject_dir in subject_dirs:
        # Find component file (any .py file except __init__.py and stories.py)
        component_files = [
            f for f in subject_dir.glob("*.py")
            if f.name not in ("__init__.py", "stories.py")
        ]
        assert len(component_files) == 1

        # Verify it has a dataclass component definition
        component_content = component_files[0].read_text()
        assert "@dataclass" in component_content
        assert "def __call__(self)" in component_content


def test_subject_stories_file_content(temp_output_dir: Path) -> None:
    """Test that subject stories.py files contain Subject definition and Story instances."""
    from storytime.__main__ import generate_catalog

    config = SizeConfig(sections=1, subjects=2, stories_per_subject=2)
    generate_catalog(temp_output_dir, config)

    section_dirs = [d for d in temp_output_dir.iterdir() if d.is_dir() and d.name.startswith("section_")]
    section = section_dirs[0]

    subject_dirs = [d for d in section.iterdir() if d.is_dir()]
    subject_dir = subject_dirs[0]

    stories_file = subject_dir / "stories.py"
    assert stories_file.exists()

    content = stories_file.read_text()
    assert "from storytime import Subject, Story" in content
    assert "def this_subject()" in content
    assert "Subject(" in content
    # Should have Story instances based on stories_per_subject
    assert "Story(" in content
