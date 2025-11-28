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

    This view implements multiple rendering modes:
    - Mode A (Custom Template): When story.template is not None, uses it for ALL rendering
    - Mode B (Default Layout): When story.template is None, renders a complete default layout
    - Mode C (Themed Iframe): When site.themed_layout is not None, wraps content in iframe

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

    def _render_badges(self) -> list[Node]:
        """Render assertion badges as tdom Nodes.

        Returns:
            List of tdom Node objects representing badges, or empty list if no badges.
        """
        # Skip badges if no assertion results
        if not self.story.assertion_results:
            return []

        badges = []
        for name, passed, error_msg in self.story.assertion_results:
            # Build styles
            base_style = "background-color: {color}; color: white; padding: 0.25rem 0.5rem; border-radius: 1rem; font-size: 0.875rem; margin-left: 0.5rem; white-space: nowrap;"

            if passed:
                # Green badge for passing assertion
                style = base_style.format(color="#4caf50")
                badge = html(
                    t'<span class="assertion-badge assertion-badge-pass success" style="{style}">{name}</span>'
                )
            else:
                # Red badge for failing assertion with tooltip
                style = base_style.format(color="#f44336") + " cursor: help;"
                if error_msg:
                    badge = html(
                        t'<span class="assertion-badge assertion-badge-fail danger" style="{style}" title="{error_msg}">{name}</span>'
                    )
                else:
                    badge = html(
                        t'<span class="assertion-badge assertion-badge-fail danger" style="{style}">{name}</span>'
                    )

            badges.append(badge)

        return badges

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

        # Render badges as tdom Nodes
        badge_nodes = self._render_badges()

        # Conditionally create description paragraph
        description_p = (
            html(t"<p>{self.story.description}</p>")
            if self.story.description
            else ""
        )

        # Mode C: Themed iframe rendering (when themed_layout is configured)
        if self.site.themed_layout is not None:
            # Wrap story content in iframe pointing to ./themed_story.html
            # Keep assertion badges in parent StoryView (not in iframe)
            iframe_style = "width: 100%; min-height: 600px; border: 1px solid #ccc;"

            if badge_nodes:
                # Header with badges and iframe
                return html(t"""\
<{Layout} view_title={self.story.title} site={self.site} depth={3} cached_navigation={self.cached_navigation}>
<div>
<div class="story-header" style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1rem;">
  <div class="story-header-left">
    <h1>{self.story.title}</h1>
  </div>
  <div class="story-header-right" style="display: flex; align-items: center; flex-wrap: wrap;">
    {badge_nodes}
  </div>
</div>
{description_p}
<p>Props: <code>{str(self.story.props)}</code></p>
<iframe src="./themed_story.html" style="{iframe_style}"></iframe>
<a href="..">Parent</a>
</div>
</{Layout}>""")
            else:
                # Header without badges and iframe
                return html(t"""\
<{Layout} view_title={self.story.title} site={self.site} depth={3} cached_navigation={self.cached_navigation}>
<div>
<h1>{self.story.title}</h1>
{description_p}
<p>Props: <code>{str(self.story.props)}</code></p>
<iframe src="./themed_story.html" style="{iframe_style}"></iframe>
<a href="..">Parent</a>
</div>
</{Layout}>""")

        # Mode B: Default layout rendering wrapped with Layout (depth=2 for story pages)
        # Use flexbox for header layout with title on left, badges on right
        if badge_nodes:
            # Header with badges (construct using tdom html)
            return html(t"""\
<{Layout} view_title={self.story.title} site={self.site} depth={3} cached_navigation={self.cached_navigation}>
<div>
<div class="story-header" style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1rem;">
  <div class="story-header-left">
    <h1>{self.story.title}</h1>
  </div>
  <div class="story-header-right" style="display: flex; align-items: center; flex-wrap: wrap;">
    {badge_nodes}
  </div>
</div>
{description_p}
<p>Props: <code>{str(self.story.props)}</code></p>
<div>
{self.story.instance}
</div>
<a href="..">Parent</a>
</div>
</{Layout}>""")
        else:
            # Header without badges (original layout)
            return html(t"""\
<{Layout} view_title={self.story.title} site={self.site} depth={3} cached_navigation={self.cached_navigation}>
<div>
<h1>{self.story.title}</h1>
{description_p}
<p>Props: <code>{str(self.story.props)}</code></p>
<div>
{self.story.instance}
</div>
<a href="..">Parent</a>
</div>
</{Layout}>""")
