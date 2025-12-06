"""Simple focused tests for assertion helpers - All Task Groups."""

import pytest
from tdom import html

from storyville.assertions import GetByTagName, GetByText, GetById


def test_get_by_tag_name_finds_element() -> None:
    """Test GetByTagName finds element."""
    helper = GetByTagName(tag_name="button")
    element = html(t"<button>Click</button>")

    helper(element)  # Should not raise


def test_get_by_text_finds_element() -> None:
    """Test GetByText finds element with text."""
    helper = GetByText(text="Submit")
    # get_by_text searches within children, so need a parent container
    element = html(t"<div><button>Submit</button></div>")

    helper(element)  # Should not raise


def test_get_by_id_finds_element() -> None:
    """Test GetById finds element by ID."""
    helper = GetById(id="main")
    element = html(t'<div id="main">Content</div>')

    helper(element)  # Should not raise


def test_not_succeeds_when_element_absent() -> None:
    """Test .not_() succeeds when element is absent."""
    helper = GetByTagName(tag_name="button").not_()
    element = html(t"<div>No button</div>")

    helper(element)  # Should not raise


def test_not_fails_when_element_present() -> None:
    """Test .not_() fails when element exists."""
    helper = GetByTagName(tag_name="button").not_()
    element = html(t"<button>Unexpected</button>")

    with pytest.raises(AssertionError) as exc_info:
        helper(element)

    assert "NOT to exist" in str(exc_info.value)


def test_text_content_verification_success() -> None:
    """Test .text_content() succeeds when text matches."""
    helper = GetByTagName(tag_name="button").text_content("Save")
    element = html(t"<button>Save</button>")

    helper(element)  # Should not raise


def test_text_content_verification_failure() -> None:
    """Test .text_content() fails when text doesn't match."""
    helper = GetByTagName(tag_name="button").text_content("Save")
    element = html(t"<button>Cancel</button>")

    with pytest.raises(AssertionError) as exc_info:
        helper(element)

    error_msg = str(exc_info.value)
    assert "Expected text:" in error_msg
    assert "Save" in error_msg
    assert "Cancel" in error_msg


def test_with_attribute_success() -> None:
    """Test .with_attribute() succeeds when attribute matches."""
    helper = GetByTagName(tag_name="button").with_attribute("type", "submit")
    element = html(t'<button type="submit">Submit</button>')

    helper(element)  # Should not raise


def test_with_attribute_missing_fails() -> None:
    """Test .with_attribute() fails when attribute missing."""
    helper = GetByTagName(tag_name="button").with_attribute("aria-pressed")
    element = html(t"<button>Toggle</button>")

    with pytest.raises(AssertionError) as exc_info:
        helper(element)

    assert "attribute" in str(exc_info.value).lower()


def test_with_attribute_wrong_value_fails() -> None:
    """Test .with_attribute() fails when attribute value is wrong."""
    helper = GetByTagName(tag_name="button").with_attribute("type", "submit")
    element = html(t'<button type="button">Click</button>')

    with pytest.raises(AssertionError) as exc_info:
        helper(element)

    error_msg = str(exc_info.value)
    assert "submit" in error_msg
    assert "button" in error_msg


def test_method_chaining() -> None:
    """Test multiple fluent methods can be chained."""
    helper = (
        GetByTagName(tag_name="button")
        .text_content("Save")
        .with_attribute("type", "button")
    )
    element = html(t'<button type="button">Save</button>')

    helper(element)  # Should not raise


def test_immutability() -> None:
    """Test fluent API maintains immutability."""
    original = GetByTagName(tag_name="button")
    modified = original.not_()

    assert original.negate is False
    assert modified.negate is True
    assert original is not modified


def test_query_failure_with_error_message() -> None:
    """Test query failure includes detailed error message."""
    helper = GetByTagName(tag_name="article")
    element = html(t"<div>No article</div>")

    with pytest.raises(AssertionError) as exc_info:
        helper(element)

    error_msg = str(exc_info.value)
    assert "article" in error_msg
    assert "Query:" in error_msg
    assert "Searched in:" in error_msg
