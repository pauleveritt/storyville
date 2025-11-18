"""FormButton component."""

from dataclasses import dataclass

from tdom import Node, html


@dataclass
class FormButton:
    """A formbutton component."""

    text: str
    variant: str
    state: str

    def __call__(self) -> Node:
        """Render the component as HTML with enhanced structure."""
        return html(t"""
            <div class="form-button-container">
                <div class="button-wrapper">
                    <div class="button-inner">
                        <button class={self.variant} data-state={self.state}>
                            <span class="button-icon-start"></span>
                            <span class="button-text">{self.text}</span>
                            <span class="button-icon-end"></span>
                        </button>
                    </div>
                    <div class="button-helper-text">Button description</div>
                </div>
            </div>
        """)
