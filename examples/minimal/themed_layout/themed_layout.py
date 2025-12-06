"""Example ThemedLayout component demonstrating custom themed rendering."""

from dataclasses import dataclass

from tdom import Node, html


@dataclass
class ThemedLayout:
    """Example themed layout component with custom styling.

    Demonstrates how to create a custom themed layout that renders
    a complete HTML document with custom CSS and branding.
    """

    story_title: str | None
    children: Node | None

    def __call__(self) -> Node:
        """Render the themed layout to a tdom Node.

        Returns:
            A tdom Node representing the complete HTML document.
        """
        # Build title
        title_text = self.story_title if self.story_title else "Themed Story"

        return html(t"""\
<!DOCTYPE html>
<html lang="EN">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{title_text}</title>
    <style>
        body {{
            font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #ffffff;
            margin: 0;
            padding: 20px;
            min-height: 100vh;
        }}
        .theme-wrapper {{
            max-width: 900px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.1);
            padding: 40px;
            border-radius: 12px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
        }}
        .theme-wrapper h1 {{
            color: #ffffff;
            margin-top: 0;
            font-size: 2rem;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
        }}
        .theme-wrapper p {{
            line-height: 1.6;
            color: rgba(255, 255, 255, 0.95);
        }}
        .theme-wrapper a {{
            color: #ffd700;
            text-decoration: underline;
        }}
    </style>
</head>
<body>
    <div class="theme-wrapper">
        {self.children}
    </div>
</body>
</html>
""")
