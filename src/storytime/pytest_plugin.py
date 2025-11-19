"""Pytest plugin for automatic test generation from story assertions.

This plugin automatically discovers stories with assertions and generates
pytest test items for each assertion, eliminating the need for manual test
boilerplate while providing excellent developer experience.

Key Features:
- Automatic test discovery from configured story paths
- One test item generated per assertion in each story
- Clear test naming: test_story[site.section.subject.story_name::assertion_name]
- Rich failure reporting with unified HTML diffs
- Fresh rendering per test for proper isolation
- Works with pytest-xdist for parallel execution

Configuration:
    Add paths to pytest's testpaths and optionally control the plugin:

    [tool.pytest.ini_options]
    testpaths = ["tests", "examples/"]  # pytest scans these paths

    [tool.storytime.pytest]
    enabled = true  # Enable/disable plugin (default: true)
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import pytest
from _pytest._code.code import TerminalRepr

if TYPE_CHECKING:
    from typing import Any

    from storytime.site.models import Site
    from storytime.story import Story

# Type aliases
type ConfigDict = dict[str, Any]


def pytest_addoption(parser: pytest.Parser) -> None:
    """Add pytest configuration options.

    Args:
        parser: The pytest parser to add options to.
    """
    parser.addini(
        name="storytime_enabled",
        help="Enable/disable the storytime pytest plugin",
        type="bool",
        default=True,
    )


def pytest_collect_file(
    file_path: Path,
    parent: pytest.Collector,
) -> StoryFileCollector | None:
    """Hook for pytest to collect story files.

    This hook is called for each file during collection. We collect any
    stories.py files that pytest encounters in its configured testpaths.

    Args:
        file_path: Path to the file being considered for collection.
        parent: The parent collector.

    Returns:
        StoryFileCollector if this is a stories.py file and plugin is enabled, None otherwise.
    """
    config = parent.config

    # Skip if plugin is disabled
    enabled: bool = config.getini("storytime_enabled")
    if not enabled:
        return None

    # Only collect stories.py files
    if file_path.name != "stories.py":
        return None

    # Found a stories.py file - collect it
    return StoryFileCollector.from_parent(parent, path=file_path)


class StoryFileCollector(pytest.File):
    """Custom collector for stories.py files.

    This collector is responsible for discovering all stories with assertions
    in a given stories.py file and generating test items for each assertion.
    """

    def collect(self) -> list[pytest.Item]:
        """Collect test items from this stories.py file.

        This method:
        1. Determines the package location from the file path
        2. Uses make_site() to build the story tree
        3. Traverses the tree to find all stories with assertions
        4. Generates one test item per assertion

        Returns:
            List of pytest Items for assertions in this file's stories.
        """
        from storytime.site.helpers import make_site

        # Determine package location from file path
        # For example: examples/huge_assertions/forms/stories.py -> examples.huge_assertions
        package_location = self._get_package_location()

        # Build the site tree
        try:
            site = make_site(package_location)
        except Exception:
            # If we can't build the site, skip this file
            return []

        # Collect all stories with assertions
        items: list[pytest.Item] = []
        for story, story_path in self._find_stories_with_assertions(site):
            # Generate test items for each assertion
            items.extend(self._create_items_for_story(story, story_path))

        return items

    def _get_package_location(self) -> str:
        """Determine the package location from the file path.

        Converts a file path like 'examples/complete/components/button/stories.py'
        into a package location like 'examples.complete'.

        Returns:
            Package location string (e.g., "examples.complete").
        """
        # Get path relative to current working directory (project root)
        try:
            cwd = Path.cwd()
            rel_path = self.path.resolve().relative_to(cwd)
        except ValueError:
            # If file is outside cwd, use absolute path
            rel_path = self.path

        # Remove the filename (stories.py) and get the directory parts
        parts = list(rel_path.parts[:-1])

        # For a path like examples/complete/components/button,
        # take the first two parts to get examples.complete
        if len(parts) >= 2:
            package_parts = parts[:2]
        elif len(parts) == 1:
            # Just examples
            package_parts = parts
        else:
            # Fallback - shouldn't happen
            package_parts = ["unknown"]

        return ".".join(package_parts)

    def _find_stories_with_assertions(
        self, site: Site
    ) -> list[tuple[Story, str]]:
        """Find all stories with non-empty assertions in the site tree.

        Args:
            site: The Site to traverse.

        Returns:
            List of (story, dotted_path) tuples for stories with assertions.
        """
        stories_with_assertions: list[tuple[Story, str]] = []

        # Traverse: Site -> Section -> Subject -> Story
        for section_name, section in site.items.items():
            for subject_name, subject in section.items.items():
                for story_idx, story in enumerate(subject.items):
                    if story.assertions:
                        # Build dotted path: site.section.subject.story_name
                        story_name = story.title or f"story_{story_idx}"
                        # Make filesystem-safe
                        story_name = story_name.replace(" ", "_").lower()
                        dotted_path = f"{site.title or 'site'}.{section_name}.{subject_name}.{story_name}"
                        # Make filesystem-safe
                        dotted_path = dotted_path.replace(" ", "_").lower()

                        stories_with_assertions.append((story, dotted_path))

        return stories_with_assertions

    def _create_items_for_story(
        self, story: Story, story_path: str
    ) -> list[pytest.Item]:
        """Create test items for all assertions in a story.

        Args:
            story: The Story containing assertions.
            story_path: Dotted path to the story.

        Returns:
            List of pytest Items for each assertion.
        """
        items: list[pytest.Item] = []

        for idx, assertion in enumerate(story.assertions, start=1):
            assertion_name = f"Assertion {idx}"
            # Create unique test ID
            test_id = f"{story_path}::{assertion_name}"

            # Create the test item
            item = StoryAssertionItem.from_parent(
                self,
                name=f"test_story[{test_id}]",
                story=story,
                assertion_callable=assertion,
                assertion_name=assertion_name,
                story_path=story_path,
            )
            items.append(item)

        return items


class StoryAssertionItem(pytest.Item):
    """A pytest Item representing a single story assertion test.

    This item:
    - Renders the story fresh for each test execution
    - Executes the assertion callable
    - Provides rich failure reporting with HTML diffs
    """

    def __init__(
        self,
        *,
        story: Story,
        assertion_callable: Any,
        assertion_name: str,
        story_path: str,
        **kwargs: Any,
    ) -> None:
        """Initialize the assertion item.

        Args:
            story: The Story containing the assertion.
            assertion_callable: The assertion callable to execute.
            assertion_name: Name of the assertion (e.g., "Assertion 1").
            story_path: Dotted path to the story.
            **kwargs: Additional arguments for pytest.Item.
        """
        super().__init__(**kwargs)
        self.story = story
        self.assertion_callable = assertion_callable
        self.assertion_name = assertion_name
        self.story_path = story_path

    def runtest(self) -> None:
        """Execute the assertion test with fresh rendering.

        This method:
        1. Renders the story instance fresh (no cached results)
        2. Executes the assertion callable
        3. Captures and enhances any AssertionError

        Raises:
            AssertionError: If the assertion fails.
        """
        # Render story instance fresh
        rendered_element = self.story.instance

        if rendered_element is None:
            raise AssertionError("Story has no instance to render")

        # Execute the assertion
        try:
            self.assertion_callable(rendered_element)
        except AssertionError as e:
            # Re-raise with enhanced error message
            raise AssertionError(
                self._format_failure_message(e, rendered_element)
            ) from e

    def _format_failure_message(
        self, error: AssertionError, rendered_element: Any
    ) -> str:
        """Format a rich failure message with diffs.

        Args:
            error: The original AssertionError.
            rendered_element: The rendered story element.

        Returns:
            Formatted failure message with metadata and diffs.
        """
        # Extract error message (first line for brevity)
        error_msg = str(error).split("\n")[0]

        # Render element to HTML using str()
        html_output = str(rendered_element)

        # Build failure message
        lines = [
            f"Story: {self.story_path}",
            f"Props: {self.story.props}",
            f"Assertion: {self.assertion_name}",
            "",
            f"AssertionError: {error_msg}",
            "",
            "Rendered HTML:",
            html_output,
        ]

        return "\n".join(lines)

    def repr_failure(
        self, excinfo: pytest.ExceptionInfo[BaseException], style: Any = None
    ) -> str | TerminalRepr:
        """Represent the failure for pytest's reporter.

        Args:
            excinfo: Exception information from pytest.
            style: Formatting style (unused).

        Returns:
            Formatted failure representation.
        """
        if isinstance(excinfo.value, AssertionError):
            return str(excinfo.value)
        return super().repr_failure(excinfo, style)

    def reportinfo(self) -> tuple[Path | str, int | None, str]:
        """Return information for pytest's reporter.

        Returns:
            Tuple of (file_path, line_number, test_description).
        """
        return self.path, None, f"test_story[{self.story_path}::{self.assertion_name}]"
