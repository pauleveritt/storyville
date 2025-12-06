"""The subject for the OverlayPopover component."""

from examples.huge_assertions.overlays.overlay_popover.overlay_popover import (
    OverlayPopover,
)
from storyville import Story, Subject


def this_subject() -> Subject:
    """Subject for OverlayPopover component."""
    return Subject(
        title="Overlay Popover",
        description="Popover overlay",
        target=OverlayPopover,
        items=[
            Story(
                props=dict(text="Default", variant="primary", state="default"),
                assertions=[
                    lambda el: None
                    if len(str(el)) > 10
                    else (_ for _ in ()).throw(AssertionError("Element too short")),
                    lambda el: None
                    if hasattr(el, "__html__")
                    else (_ for _ in ()).throw(
                        AssertionError("Missing __html__ attribute")
                    ),
                    lambda el: None
                    if el is not None
                    else (_ for _ in ()).throw(AssertionError("Element is None")),
                ],
            ),
            Story(
                props=dict(text="Disabled", variant="secondary", state="disabled"),
                assertions=[
                    lambda el: None
                    if str(el).find("<") != -1
                    else (_ for _ in ()).throw(AssertionError("No HTML tags found"))
                ],
            ),
            Story(
                props=dict(text="Loading", variant="primary", state="loading"),
                assertions=[
                    lambda el: None
                    if any(tag in str(el) for tag in ["div", "span", "button", "input"])
                    else (_ for _ in ()).throw(AssertionError("No common tags"))
                ],
            ),
        ],
    )
