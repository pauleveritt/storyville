"""Test the Section class."""

from storytime.section import Section
from storytime.site import Site
from storytime.story import Subject


def test_section_initialization() -> None:
    """Test Section can be instantiated."""
    section = Section(title="Components")
    assert section.title == "Components"
    assert section.parent is None
    assert section.items == {}


def test_section_with_parent() -> None:
    """Test Section with parent site."""
    site = Site(title="My Site")
    section = Section(title="Components", parent=site)
    assert section.parent is site


def test_section_with_subjects() -> None:
    """Test Section with subjects."""
    subject1 = Subject(title="Heading")
    subject2 = Subject(title="Button")
    section = Section(title="Components")
    section.items["heading"] = subject1
    section.items["button"] = subject2

    assert len(section.items) == 2
    assert section.items["heading"] is subject1
    assert section.items["button"] is subject2
