"""The subject for the DataChart component."""

from examples.huge_assertions.data_display.data_chart.data_chart import DataChart
from storytime import Story, Subject


def this_subject() -> Subject:
    """Subject for DataChart component."""
    return Subject(
        title="Data Chart",
        description="Chart display",
        target=DataChart,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default"), assertions=[lambda el: None if any(tag in str(el) for tag in ["div", "span", "button", "input"]) else (_ for _ in ()).throw(AssertionError("No common tags")), lambda el: None if el is not None else (_ for _ in ()).throw(AssertionError("Element is None"))]),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading"), assertions=[lambda el: None if str(el).find("<") != -1 else (_ for _ in ()).throw(AssertionError("No HTML tags found"))]),
        ],
    )
