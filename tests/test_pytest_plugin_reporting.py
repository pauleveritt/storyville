"""Tests for pytest plugin failure reporting."""


def test_assertion_error_capture():
    """Test that AssertionError is properly captured."""
    error = AssertionError("Test error message")
    error_msg = str(error)

    assert "Test error message" in error_msg


def test_error_message_extraction():
    """Test that error message is extracted correctly."""
    error = AssertionError("First line\nSecond line")
    # Extract first line
    error_msg = str(error).split("\n")[0]

    assert error_msg == "First line"


def test_html_rendering():
    """Test that story instance can be rendered to HTML."""
    from tdom import html

    # Create a simple element
    element = html(t"<div>Test content</div>")

    # Serialize to HTML using str()
    html_output = str(element)

    assert "div" in html_output
    assert "Test content" in html_output


def test_failure_message_includes_metadata():
    """Test that failure messages include required metadata."""
    story_path = "site.section.subject.story"
    props = {"text": "Test", "variant": "primary"}
    assertion_name = "Assertion 1"
    error_msg = "No common tags"

    # Build failure message structure
    lines = [
        f"Story: {story_path}",
        f"Props: {props}",
        f"Assertion: {assertion_name}",
        "",
        f"AssertionError: {error_msg}",
    ]
    message = "\n".join(lines)

    # Verify all metadata is included
    assert story_path in message
    assert "Props:" in message
    assert assertion_name in message
    assert error_msg in message
