"""The subject for the DataStat component."""

from examples.huge_assertions.data_display.data_stat.data_stat import DataStat
from storyville import Story, Subject


def this_subject() -> Subject:
    """Subject for DataStat component."""
    return Subject(
        title="Data Stat",
        description="Statistic display",
        target=DataStat,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled"), assertions=[lambda el: None if (el is not None and str(el)) else (_ for _ in ()).throw(AssertionError("Invalid element")), lambda el: None if el is not None else (_ for _ in ()).throw(AssertionError("Element is None")), lambda el: None if any(tag in str(el) for tag in ["div", "span", "button", "input"]) else (_ for _ in ()).throw(AssertionError("No common tags"))]),
            Story(props=dict(text="Loading", variant="primary", state="loading"), assertions=[lambda el: None if any(tag in str(el) for tag in ["div", "span", "button", "input"]) else (_ for _ in ()).throw(AssertionError("No common tags"))]),
        ],
    )
