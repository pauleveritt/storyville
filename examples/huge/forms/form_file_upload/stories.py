"""The subject for the FormFileUpload component."""

from examples.huge.forms.form_file_upload.form_file_upload import FormFileUpload
from storytime import Story, Subject


def this_subject() -> Subject:
    """Subject for FormFileUpload component."""
    return Subject(
        title="Form File Upload",
        description="File upload for forms",
        target=FormFileUpload,
        items=[
            Story(props=dict(text="Default", variant="primary", state="default")),
            Story(props=dict(text="Disabled", variant="secondary", state="disabled")),
            Story(props=dict(text="Loading", variant="primary", state="loading")),
        ],
    )
