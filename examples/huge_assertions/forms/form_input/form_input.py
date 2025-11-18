"""FormInput component."""

from dataclasses import dataclass

from tdom import Node, html


@dataclass
class FormInput:
    """A form input component."""

    text: str
    variant: str
    state: str

    def __call__(self) -> Node:
        """Render the component as HTML with enhanced structure."""
        return html(t"""
            <div class="form-input-container">
                <div class="input-wrapper">
                    <label class="input-label">{self.text}</label>
                    <div class="input-field-wrapper">
                        <span class="input-prefix"></span>
                        <input type="text" class={self.variant} data-state={self.state} />
                        <span class="input-suffix"></span>
                    </div>
                    <div class="input-validation-message"></div>
                </div>
            </div>
        """)
