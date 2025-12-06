"""Tests for list-oriented query helpers (GetAllBy*)."""

import pytest
from tdom import html

from storyville.assertions import (
    GetAllByClass,
    GetAllByLabelText,
    GetAllByRole,
    GetAllByTagName,
    GetAllByTestId,
    GetAllByText,
)


def test_get_all_by_role_returns_list() -> None:
    """Test GetAllByRole finds multiple elements."""
    helper = GetAllByRole(role="button")
    element = html(
        t"""<div>
        <button>First</button>
        <button>Second</button>
        <button>Third</button>
    </div>"""
    )

    helper(element)  # Should not raise


def test_get_all_by_text_multiple_matches() -> None:
    """Test GetAllByText finds all matching text elements."""
    helper = GetAllByText(text="Item")
    element = html(
        t"""<ul>
        <li>Item</li>
        <li>Item</li>
        <li>Item</li>
    </ul>"""
    )

    helper(element)  # Should not raise


def test_count_assertion_success() -> None:
    """Test .count() succeeds when count matches."""
    helper = GetAllByRole(role="button").count(2)
    element = html(
        t"""<div>
        <button>First</button>
        <button>Second</button>
    </div>"""
    )

    helper(element)  # Should not raise


def test_count_assertion_failure() -> None:
    """Test .count() fails when count doesn't match."""
    helper = GetAllByRole(role="button").count(2)
    element = html(
        t"""<div>
        <button>First</button>
        <button>Second</button>
        <button>Third</button>
    </div>"""
    )

    with pytest.raises(AssertionError) as exc_info:
        helper(element)

    error_msg = str(exc_info.value)
    assert "Expected count: 2" in error_msg
    assert "found: 3" in error_msg


def test_nth_selection_with_text_content() -> None:
    """Test .nth() selects element and chains to .text_content()."""
    helper = GetAllByRole(role="button").nth(1).text_content("Second")
    element = html(
        t"""<div>
        <button>First</button>
        <button>Second</button>
        <button>Third</button>
    </div>"""
    )

    helper(element)  # Should not raise


def test_nth_selection_with_attribute() -> None:
    """Test .nth() selects element and chains to .with_attribute()."""
    helper = GetAllByRole(role="button").nth(0).with_attribute("type", "submit")
    element = html(
        t"""<div>
        <button type="submit">First</button>
        <button type="button">Second</button>
    </div>"""
    )

    helper(element)  # Should not raise


def test_nth_out_of_bounds_error() -> None:
    """Test .nth() raises error for out-of-bounds index."""
    helper = GetAllByRole(role="button").nth(5)
    element = html(
        t"""<div>
        <button>First</button>
        <button>Second</button>
    </div>"""
    )

    with pytest.raises(AssertionError) as exc_info:
        helper(element)

    error_msg = str(exc_info.value)
    assert "Index 5 out of bounds" in error_msg
    assert "found 2 elements" in error_msg


def test_get_all_by_tag_name() -> None:
    """Test GetAllByTagName finds all matching tag elements."""
    helper = GetAllByTagName(tag_name="li").count(3)
    element = html(
        t"""<ul>
        <li>One</li>
        <li>Two</li>
        <li>Three</li>
    </ul>"""
    )

    helper(element)  # Should not raise


def test_get_all_by_class() -> None:
    """Test GetAllByClass finds all elements with class."""
    helper = GetAllByClass(class_name="item").count(2)
    element = html(
        t"""<div>
        <span class="item">First</span>
        <span class="item">Second</span>
    </div>"""
    )

    helper(element)  # Should not raise


def test_get_all_by_test_id() -> None:
    """Test GetAllByTestId finds all elements with test ID."""
    helper = GetAllByTestId(test_id="card").count(2)
    element = html(
        t"""<div>
        <div data-testid="card">Card 1</div>
        <div data-testid="card">Card 2</div>
    </div>"""
    )

    helper(element)  # Should not raise


def test_get_all_by_label_text() -> None:
    """Test GetAllByLabelText finds all labeled elements."""
    helper = GetAllByLabelText(label="Option").count(2)
    element = html(
        t"""<form>
        <label>Option<input type="checkbox" /></label>
        <label>Option<input type="checkbox" /></label>
    </form>"""
    )

    helper(element)  # Should not raise


def test_empty_list_error_message() -> None:
    """Test error message when no elements found."""
    helper = GetAllByRole(role="button")
    element = html(t"<div>No buttons here</div>")

    with pytest.raises(AssertionError) as exc_info:
        helper(element)

    error_msg = str(exc_info.value)
    assert "button" in error_msg.lower()
    assert "Query:" in error_msg


def test_nth_with_method_chaining() -> None:
    """Test .nth() works with multiple chained methods."""
    helper = (
        GetAllByRole(role="button")
        .nth(1)
        .text_content("Submit")
        .with_attribute("disabled", "true")
    )
    element = html(
        t"""<div>
        <button>Cancel</button>
        <button disabled="true">Submit</button>
    </div>"""
    )

    helper(element)  # Should not raise


def test_count_zero() -> None:
    """Test .count(0) verifies no elements exist."""
    helper = GetAllByRole(role="button").count(0)
    element = html(t"<div>No buttons</div>")

    with pytest.raises(AssertionError) as exc_info:
        helper(element)

    # Since aria-testing get_all_by_* raises error when no elements found,
    # we expect the standard not-found error message
    error_msg = str(exc_info.value)
    assert "button" in error_msg.lower()
