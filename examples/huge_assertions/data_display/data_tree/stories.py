"""The subject for the DataTree component."""

from examples.huge_assertions.data_display.data_tree.data_tree import DataTree
from storyville import Story, Subject


def this_subject() -> Subject:
    """Subject for DataTree component."""
    return Subject(
        title="Data Tree",
        description="Tree structure",
        target=DataTree,
        items=[
            Story(
                props=dict(text="Default", variant="primary", state="default"),
                assertions=[
                    lambda el: None
                    if str(el).find("<") != -1
                    else (_ for _ in ()).throw(AssertionError("No HTML tags found")),
                    lambda el: None
                    if hasattr(el, "__html__")
                    else (_ for _ in ()).throw(
                        AssertionError("Missing __html__ attribute")
                    ),
                ],
            ),
            Story(
                props=dict(text="Disabled", variant="secondary", state="disabled"),
                assertions=[
                    lambda el: None
                    if len(str(el)) > 10
                    else (_ for _ in ()).throw(AssertionError("Element too short")),
                    lambda el: None
                    if str(el).find("<") != -1
                    else (_ for _ in ()).throw(AssertionError("No HTML tags found")),
                ],
            ),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
