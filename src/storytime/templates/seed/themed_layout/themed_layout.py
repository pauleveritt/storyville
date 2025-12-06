"""Custom themed layout component for the generated catalog."""

from dataclasses import dataclass

from tdom import Node, html


@dataclass
class ThemedLayout:
    """A custom themed layout demonstrating Storytime layout customization.

    This layout wraps story content in a full HTML document with custom styling,
    showing how to create branded or design-system-specific layouts for your
    component stories.

    Args:
        story_title: The title of the story being rendered.
        children: The child nodes to render within the layout.
    """

    story_title: str | None
    children: Node | None

    def __call__(self) -> Node:
        """Render the themed layout using tdom t-string.

        Returns:
            Node: The complete HTML document with themed styling.
        """
        title_text = self.story_title if self.story_title else "Story"

        return html(t'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{title_text}</title>
    <style>
        body {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            font-family: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
            margin: 0;
            padding: 20px;
            min-height: 100vh;
        }}
        .story-wrapper {{
            max-width: 900px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.95);
            padding: 40px;
            border-radius: 12px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        }}
        .story-wrapper h1 {{
            color: #667eea;
            margin-top: 0;
        }}
    </style>
</head>
<body>
    <div class="story-wrapper">
        {self.children}
    </div>
</body>
</html>
''')
