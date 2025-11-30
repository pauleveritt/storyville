"""Tests for NavigationTree component."""

from aria_testing import get_by_tag_name, get_text_content, query_all_by_tag_name
from storytime.components.navigation_tree import NavigationTree
from storytime.section import Section
from storytime.story import Story
from storytime.subject import Subject

def test_renders_three_level_hierarchy():
    """NavigationTree renders sections, subjects, and stories."""
    # Create a simple hierarchy
    section = Section(name="components", title="Components")
    subject = Subject(name="buttons", title="Buttons", parent=section)
    story = Story(title="Primary Button", parent=subject)

    subject.items = [story]
    section.items = {"buttons": subject}
    sections = {"components": section}

    tree = NavigationTree(sections=sections, resource_path=None)
    result = tree()

    # Find the nav element (handles both Element and Fragment)
    nav = get_by_tag_name(result, "nav")
    assert nav is not None

    # Should have section details with summary
    details_list = query_all_by_tag_name(result, "details")
    assert len(details_list) >= 1

    # Should have summaries (section + subject)
    summaries = query_all_by_tag_name(result, "summary")
    summary_texts = [get_text_content(s) for s in summaries]
    assert "Components" in summary_texts

    # Should have story as link
    links = query_all_by_tag_name(result, "a")
    assert len(links) >= 1
    assert get_text_content(links[0]) == "Primary Button"

def test_details_elements_use_correct_structure():
    """Sections and subjects use details/summary elements."""
    section = Section(name="layout", title="Layout")
    subject = Subject(name="grid", title="Grid", parent=section)
    story = Story(title="Basic Grid", parent=subject)

    subject.items = [story]
    section.items = {"grid": subject}
    sections = {"layout": section}

    tree = NavigationTree(sections=sections, resource_path=None)
    result = tree()

    # Should have details elements (section + subject = 2)
    details_list = query_all_by_tag_name(result, "details")
    assert len(details_list) == 2

    # Should have summary elements (section + subject = 2)
    summaries = query_all_by_tag_name(result, "summary")
    assert len(summaries) == 2
    summary_texts = [get_text_content(s) for s in summaries]
    assert "Layout" in summary_texts
    assert "Grid" in summary_texts

    # Should have link for story
    link = get_by_tag_name(result, "a")
    assert get_text_content(link) == "Basic Grid"

def test_resource_path_controls_open_attribute():
    """Only the current path's ancestors have open attribute."""
    section = Section(name="forms", title="Forms")
    subject = Subject(name="inputs", title="Inputs", parent=section)
    story = Story(title="Text Input", parent=subject)

    subject.items = [story]
    section.items = {"inputs": subject}
    sections = {"forms": section}

    # Test with resource_path matching this section and subject
    tree = NavigationTree(sections=sections, resource_path="forms/inputs")
    result = tree()

    # Section details should have 'open' attribute
    details_list = query_all_by_tag_name(result, "details")
    section_details = details_list[0]  # First details is the section
    assert section_details.attrs.get("open") == "open"

    # Subject details should also have 'open' attribute
    subject_details = details_list[1]  # Second details is the subject
    assert subject_details.attrs.get("open") == "open"

def test_all_details_closed_when_resource_path_none():
    """When resource_path is None, all details are closed by default."""
    section = Section(name="typography", title="Typography")
    subject = Subject(name="headings", title="Headings", parent=section)
    story = Story(title="H1", parent=subject)

    subject.items = [story]
    section.items = {"headings": subject}
    sections = {"typography": section}

    tree = NavigationTree(sections=sections, resource_path=None)
    result = tree()

    # All details should NOT have 'open' attribute
    details_list = query_all_by_tag_name(result, "details")
    for details in details_list:
        assert details.attrs.get("open") is None

def test_stories_render_as_simple_links():
    """Stories are simple li/a elements, not collapsible."""
    section = Section(name="navigation", title="Navigation")
    subject = Subject(name="menus", title="Menus", parent=section)
    story1 = Story(title="Dropdown Menu", parent=subject)
    story2 = Story(title="Sidebar Menu", parent=subject)

    subject.items = [story1, story2]
    section.items = {"menus": subject}
    sections = {"navigation": section}

    tree = NavigationTree(sections=sections, resource_path=None)
    result = tree()

    # Should have exactly 2 details elements (1 section + 1 subject)
    # Stories should NOT add details elements
    details_list = query_all_by_tag_name(result, "details")
    assert len(details_list) == 2

    # Should have 2 story links
    links = query_all_by_tag_name(result, "a")
    assert len(links) == 2
    link_texts = [get_text_content(link) for link in links]
    assert "Dropdown Menu" in link_texts
    assert "Sidebar Menu" in link_texts

def test_section_open_when_resource_path_starts_with_section_name():
    """Section gets open attribute if resource_path starts with section name."""
    section1 = Section(name="sec1", title="Section 1")
    section2 = Section(name="sec2", title="Section 2")
    subject1 = Subject(name="subj1", title="Subject 1", parent=section1)
    subject2 = Subject(name="subj2", title="Subject 2", parent=section2)

    section1.items = {"subj1": subject1}
    section2.items = {"subj2": subject2}
    sections = {"sec1": section1, "sec2": section2}

    tree = NavigationTree(sections=sections, resource_path="sec1/subj1")
    result = tree()

    # Get all details elements
    details_list = query_all_by_tag_name(result, "details")

    # First two details are for sec1 (section) and subj1 (subject)
    # They should be open
    assert details_list[0].attrs.get("open") == "open"  # sec1
    assert details_list[1].attrs.get("open") == "open"  # subj1

    # Last two details are for sec2 (section) and subj2 (subject)
    # They should be closed
    assert details_list[2].attrs.get("open") is None  # sec2
    assert details_list[3].attrs.get("open") is None  # subj2

def test_subject_open_when_resource_path_matches_section_subject():
    """Subject gets open attribute if resource_path matches section/subject."""
    section = Section(name="components", title="Components")
    subject1 = Subject(name="buttons", title="Buttons", parent=section)
    subject2 = Subject(name="inputs", title="Inputs", parent=section)
    story = Story(title="Primary", parent=subject1)

    subject1.items = [story]
    subject2.items = []
    section.items = {"buttons": subject1, "inputs": subject2}
    sections = {"components": section}

    tree = NavigationTree(sections=sections, resource_path="components/buttons")
    result = tree()

    # Get all details elements
    details_list = query_all_by_tag_name(result, "details")

    # Section (components) should be open
    assert details_list[0].attrs.get("open") == "open"

    # First subject (buttons) should be open
    assert details_list[1].attrs.get("open") == "open"

    # Second subject (inputs) should be closed
    assert details_list[2].attrs.get("open") is None

def test_story_urls_use_index_html_format():
    """Story URLs should use /story-{idx}/index.html format, not /story-{idx}.html."""
    section = Section(name="components", title="Components")
    subject = Subject(name="heading", title="Heading", parent=section)
    story = Story(title="Basic Heading", parent=subject)

    subject.items = [story]
    section.items = {"heading": subject}
    sections = {"components": section}

    tree = NavigationTree(sections=sections, resource_path=None)
    result = tree()

    # Get the story link
    links = query_all_by_tag_name(result, "a")
    assert len(links) == 1
    link = links[0]

    # Verify URL format is /section/subject/story-0/index.html
    assert link.attrs.get("href") == "/components/heading/story-0/index.html"

def test_multiple_stories_have_correct_url_indices():
    """Multiple stories should have incrementing indices in their URLs."""
    section = Section(name="components", title="Components")
    subject = Subject(name="button", title="Button", parent=section)
    story0 = Story(title="Primary", parent=subject)
    story1 = Story(title="Secondary", parent=subject)
    story2 = Story(title="Tertiary", parent=subject)

    subject.items = [story0, story1, story2]
    section.items = {"button": subject}
    sections = {"components": section}

    tree = NavigationTree(sections=sections, resource_path=None)
    result = tree()

    # Get all story links
    links = query_all_by_tag_name(result, "a")
    assert len(links) == 3

    # Verify each URL has correct index
    assert links[0].attrs.get("href") == "/components/button/story-0/index.html"
    assert links[1].attrs.get("href") == "/components/button/story-1/index.html"
    assert links[2].attrs.get("href") == "/components/button/story-2/index.html"

def test_story_urls_use_section_and_subject_names():
    """Story URLs should incorporate section and subject names."""
    section = Section(name="forms", title="Forms")
    subject = Subject(name="inputs", title="Inputs", parent=section)
    story = Story(title="Text Input", parent=subject)

    subject.items = [story]
    section.items = {"inputs": subject}
    sections = {"forms": section}

    tree = NavigationTree(sections=sections, resource_path=None)
    result = tree()

    # Get the story link
    link = get_by_tag_name(result, "a")

    # Verify URL uses section and subject names
    href = link.attrs.get("href")
    assert href == "/forms/inputs/story-0/index.html"
    assert "/forms/" in href
    assert "/inputs/" in href
