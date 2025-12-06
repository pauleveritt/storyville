"""Tests for assertion helpers foundation - Task Group 1."""

from dataclasses import FrozenInstanceError

import pytest
from tdom import html

from storyville.assertions.helpers import GetByTagName


def test_helper_is_frozen_dataclass() -> None:
    """Test helper classes are frozen dataclasses (immutable)."""
    helper = GetByTagName(tag_name="div")

    # Attempting to modify should raise FrozenInstanceError
    with pytest.raises(FrozenInstanceError):
        helper.tag_name = "span"  # type: ignore


def test_helper_call_signature_accepts_element() -> None:
    """Test __call__ accepts Element type."""
    helper = GetByTagName(tag_name="div")
    element = html(t"<div>Test</div>")

    # Should not raise - element exists
    helper(element)


def test_helper_call_signature_accepts_fragment() -> None:
    """Test __call__ accepts Fragment type."""
    helper = GetByTagName(tag_name="span")
    fragment = html(t"<div><span>Test</span></div>")

    # Should not raise - element exists in fragment
    helper(fragment)


def test_helper_raises_assertion_error_on_query_failure() -> None:
    """Test __call__ raises AssertionError when element not found."""
    helper = GetByTagName(tag_name="button")
    element = html(t"<div>No button here</div>")

    with pytest.raises(AssertionError) as exc_info:
        helper(element)

    # Error message should mention what we were looking for
    assert "button" in str(exc_info.value)


def test_helper_passes_query_parameters() -> None:
    """Test helper correctly passes query parameters to aria-testing."""
    helper = GetByTagName(tag_name="input")
    element = html(t"<form><input type='text' /></form>")

    # Should find the input element
    helper(element)


def test_helper_detailed_error_message() -> None:
    """Test error message includes search criteria and context."""
    helper = GetByTagName(tag_name="article")
    element = html(t"<div><p>Content</p></div>")

    with pytest.raises(AssertionError) as exc_info:
        helper(element)

    error_msg = str(exc_info.value)
    # Should include what we searched for
    assert "article" in error_msg
    # Should provide context about the search
    assert "Unable to find" in error_msg or "not found" in error_msg.lower()


def test_module_imports_work() -> None:
    """Test that module imports work correctly."""
    from storyville.assertions import GetByTagName as ImportedHelper

    helper = ImportedHelper(tag_name="div")
    element = html(t"<div>Test</div>")
    helper(element)
