"""Test the Section model."""

from storytime.section.models import Section
from storytime.site import Site
from storytime.subject import Subject


def test_section_initialization() -> None:
    """Test Section can be instantiated."""
    section = Section(title="Components")
    assert section.title == "Components"
    assert section.parent is None
    assert section.items == {}
    assert section.description is None


def test_section_with_parent() -> None:
    """Test Section with parent site."""
    site = Site(title="My Site")
    section = Section(title="Components", parent=site)
    assert section.parent is site


def test_section_with_description() -> None:
    """Test Section with description field."""
    section = Section(title="Components", description="UI component library")
    assert section.description == "UI component library"


def test_section_with_items() -> None:
    """Test Section with items dict."""
    subject1 = Subject(title="Button")
    subject2 = Subject(title="Input")
    section = Section(
        title="Components",
        items={"button": subject1, "input": subject2}
    )

    assert len(section.items) == 2
    assert section.items["button"] is subject1
    assert section.items["input"] is subject2
