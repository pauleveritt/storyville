"""StoryView for rendering Story instances with dual modes."""

import logging
from dataclasses import dataclass

from tdom import Node, html

from storytime.components.layout import Layout
from storytime.site.models import Site
from storytime.story.models import Story

logger = logging.getLogger(__name__)


@dataclass
class StoryView:
    """View for rendering a Story with custom template or default layout.

    This view implements dual rendering modes:
    - Mode A (Custom Template): When story.template is not None, uses it for ALL rendering
    - Mode B (Default Layout): When story.template is None, renders a complete default layout

    The view satisfies the View Protocol by implementing __call__() -> Node.
    Tests use type guards to verify the result is an Element.
    """

    story: Story
    site: Site
    cached_navigation: str | None = None
    with_assertions: bool = True

    def _execute_assertions(self, with_assertions: bool = True) -> None:
        """Execute assertions against the rendered story instance.

        Args:
            with_assertions: Whether to execute assertions (default: True)
        """
        # Skip if assertions disabled or no assertions defined
        if not with_assertions or not self.story.assertions:
            return

        # Get rendered element from story instance
        rendered_element = self.story.instance
        if rendered_element is None:
            return

        # Execute each assertion and collect results
        results = []
        for i, assertion in enumerate(self.story.assertions, start=1):
            name = f"Assertion {i}"
            try:
                # Pass rendered element to assertion
                assertion(rendered_element)
                # Assertion passed (no exception raised)
                results.append((name, True, None))
            except AssertionError as e:
                # Expected assertion failure
                error_msg = str(e).split("\n")[0]  # First line only
                results.append((name, False, error_msg))
            except Exception as e:
                # Critical error (unexpected exception)
                error_msg = f"Critical error: {str(e).split('\n')[0]}"
                results.append((name, False, error_msg))
                # Log full exception for debugging
                logger.error(f"Critical error in {name}: {e}", exc_info=True)

        # Store results on story for later rendering
        self.story.assertion_results = results

    def __call__(self) -> Node:
        """Render the story to a tdom Node.

        Returns:
            A tdom Node representing the rendered story.
        """
        # Execute assertions if enabled (after story.instance is available)
        self._execute_assertions(with_assertions=self.with_assertions)

        # Mode A: Custom template rendering
        if self.story.template is not None:
            return self.story.template()

        # Mode B: Default layout rendering wrapped with Layout (depth=2 for story pages)
        return html(t"""\
<{Layout} view_title={self.story.title} site={self.site} depth={2} cached_navigation={self.cached_navigation}>
<div>
<h1>{self.story.title}</h1>
<p>Props: <code>{str(self.story.props)}</code></p>
<div>
{self.story.instance}
</div>
<a href="..">Parent</a>
</div>
</{Layout}>""")
