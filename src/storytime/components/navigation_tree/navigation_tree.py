"""NavigationTree component for hierarchical sidebar navigation."""

from dataclasses import dataclass

from tdom import Node, html

from storytime.section.models import Section


def parse_current_path(path: str | None) -> tuple[str | None, str | None, str | None]:
    """Parse current_path into section, subject, story components.

    Args:
        path: Path string in format "section/subject/story" or None.

    Returns:
        Tuple of (section_name, subject_name, story_name), each can be None.
    """
    match path:
        case None | "":
            return (None, None, None)
        case str(p):
            parts = p.split("/")
            match len(parts):
                case 1:
                    return (parts[0], None, None)
                case 2:
                    return (parts[0], parts[1], None)
                case n if n >= 3:
                    return (parts[0], parts[1], parts[2])
                case _:
                    return (None, None, None)
        case _:
            return (None, None, None)


@dataclass
class NavigationTree:
    """Hierarchical navigation tree for sections, subjects, and stories.

    Renders a three-level collapsible navigation using HTML5 details/summary
    elements without JavaScript. Sections and subjects are collapsible,
    while stories are simple links.
    """

    sections: dict[str, Section]
    current_path: str | None = None

    def __call__(self) -> Node:
        """Render the navigation tree to a tdom Node.

        Returns:
            A tdom Node representing the navigation structure.
        """
        section_name, subject_name, _story_name = parse_current_path(self.current_path)

        # Build section items
        section_items = []
        for sec_key, section in self.sections.items():
            # Determine if this section should be open
            section_open = section_name == sec_key

            # Build subject items for this section
            subject_items = []
            for subj_key, subject in section.items.items():
                # Determine if this subject should be open
                subject_open = section_open and subject_name == subj_key

                # Build story links for this subject
                story_links = []
                for idx, story in enumerate(subject.items):
                    # Build URL for story
                    # Format: /{section}/{subject}/story-{idx}/index.html
                    story_url = f"/{sec_key}/{subj_key}/story-{idx}/index.html"
                    story_title = story.title or f"Story {idx}"
                    story_links.append(
                        html(
                            t'<li><a href="{story_url}">{story_title}</a></li>'
                        )
                    )

                # Render subject as nested details
                if subject_open:
                    subject_html = html(t'''
                        <li>
                          <details open="open">
                            <summary>{subject.title}</summary>
                            <ul>
                              {story_links}
                            </ul>
                          </details>
                        </li>
                    ''')
                else:
                    subject_html = html(t'''
                        <li>
                          <details>
                            <summary>{subject.title}</summary>
                            <ul>
                              {story_links}
                            </ul>
                          </details>
                        </li>
                    ''')
                subject_items.append(subject_html)

            # Render section as top-level details
            if section_open:
                section_html = html(t'''
                    <details open="open">
                      <summary>{section.title}</summary>
                      <ul>
                        {subject_items}
                      </ul>
                    </details>
                ''')
            else:
                section_html = html(t'''
                    <details>
                      <summary>{section.title}</summary>
                      <ul>
                        {subject_items}
                      </ul>
                    </details>
                ''')
            section_items.append(section_html)

        # Return navigation with all sections
        return html(t'''
            <nav>
              {section_items}
            </nav>
        ''')
