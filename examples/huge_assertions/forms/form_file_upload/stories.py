"""The subject for the FormFileUpload component."""

from examples.huge_assertions.forms.form_file_upload.form_file_upload import FormFileUpload
from storyville import Story, Subject


def this_subject() -> Subject:
    """Subject for FormFileUpload component."""
    return Subject(
        title="Form File Upload",
        description="File upload for forms",
        target=FormFileUpload,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default"), assertions=[lambda el: None if any(tag in str(el) for tag in ["div", "span", "button", "input"]) else (_ for _ in ()).throw(AssertionError("No common tags")), lambda el: None if (el is not None and str(el)) else (_ for _ in ()).throw(AssertionError("Invalid element"))]),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled"), assertions=[lambda el: None if (el is not None and str(el)) else (_ for _ in ()).throw(AssertionError("Invalid element"))]),
            Story(props=dict(text="Loading", variant="primary", state="loading"), assertions=[lambda el: None if "class" in str(el).lower() or "div" in str(el).lower() else (_ for _ in ()).throw(AssertionError("No class or div found")), lambda el: None if any(tag in str(el) for tag in ["div", "span", "button", "input"]) else (_ for _ in ()).throw(AssertionError("No common tags")), lambda el: None if (el is not None and str(el)) else (_ for _ in ()).throw(AssertionError("Invalid element"))]),
        ],
    )
