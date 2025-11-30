"""Breadcrumb navigation component."""

from dataclasses import dataclass

from tdom import Node, html

from storytime.components.navigation_tree import parse_current_path


@dataclass
class Breadcrumbs:
    """Breadcrumb navigation component showing path hierarchy.

    Renders breadcrumb trail from Home to current page, with all items
    as clickable links except the current (last) item. Uses " > " as separator.
    All links use relative paths based on current depth.
    """

    resource_path: str = ""

    def __call__(self) -> Node:
        """Render the breadcrumbs to a tdom Node.

        Returns:
            A tdom Node representing the breadcrumb navigation.
        """
        # If no resource_path, render nothing
        if not self.resource_path:
            return html(t"")

        # Parse the path to get components
        section_name, subject_name, story_name = parse_current_path(self.resource_path)

        # Calculate depth: count non-empty path segments
        depth = len([p for p in self.resource_path.split("/") if p])

        # Calculate relative root path: "../" * depth
        relative_root = "../" * depth

        # Build breadcrumb items
        breadcrumb_items = []

        # Always include Home as first breadcrumb (link unless we're on home)
        # Since we have a resource_path, we're never on home, so it's always a link
        breadcrumb_items.append(html(t'<a href="{relative_root}">Home</a>'))

        # Add section if present
        if section_name:
            # Section is a link unless it's the current (last) item
            if subject_name is None and story_name is None:
                # Current page is section level (no subject or story)
                breadcrumb_items.append(html(t"<span>{section_name}</span>"))
            else:
                # Section is an ancestor, make it a link using relative path
                section_url = f"{relative_root}{section_name}/"
                breadcrumb_items.append(
                    html(t'<a href="{section_url}">{section_name}</a>')
                )

        # Add subject if present
        if subject_name:
            # Subject is a link unless it's the current (last) item
            if story_name is None:
                # Current page is subject level (no story)
                breadcrumb_items.append(html(t"<span>{subject_name}</span>"))
            else:
                # Subject is an ancestor, make it a link using relative path
                # From story level (depth 3), we go up one level: ../
                subject_url = "../"
                breadcrumb_items.append(
                    html(t'<a href="{subject_url}">{subject_name}</a>')
                )

        # Add story if present (always the current page, never a link)
        if story_name:
            breadcrumb_items.append(html(t"<span>{story_name}</span>"))

        # Join items with " > " separator
        # Build the breadcrumb trail with separators
        trail_items = []
        for idx, item in enumerate(breadcrumb_items):
            if idx > 0:
                # Add separator before each item except the first
                trail_items.append(html(t"<span> &gt; </span>"))
            trail_items.append(item)

        # Render breadcrumbs in nav with aria-label
        # Wrap trail_items in a span to prevent flexbox spreading
        return html(t'''
            <nav aria-label="Breadcrumb">
              <span style="display: inline;">{trail_items}</span>
            </nav>
        ''')
