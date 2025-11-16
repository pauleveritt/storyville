"""The subject for this Alert component."""

from __future__ import annotations

from tdom import Node, html

from examples.templates.components.alert.alert import Alert
from storytime import Story, Subject


def custom_alert_template() -> Node:
    """Custom template that completely overrides Story rendering.

    This demonstrates how a template has full control over rendering,
    bypassing the default StoryView layout entirely.
    """
    return html(t"<div class='custom'><h1>Custom Template</h1><p>Full control</p></div>")


def this_subject() -> Subject:
    """Let's make a Storytime subject for this Alert component."""
    return Subject(
        title="Alert",
        description="An alert component demonstrating template override behavior",
        target=Alert,
        items=[
            # Story 1: No template - uses default StoryView layout
            Story(props={"message": "This is an alert using default layout"}),
            # Story 2: Custom template - overrides all rendering
            Story(
                props={"message": "This message won't be shown"},
                template=custom_alert_template,
            ),
        ],
    )
