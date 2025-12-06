"""The Overlays section for the huge example."""


from storyville import Section


def this_section() -> Section:
    """Overlays section with overlay components."""
    return Section(
        title="Overlays",
        description="Overlay components",
    )
