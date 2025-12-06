"""Data models for static asset management."""

from dataclasses import dataclass
from pathlib import Path
from typing import Literal


@dataclass
class StaticFolder:
    """Represents a discovered static folder with metadata for copying.

    This dataclass tracks information about a static folder including its source
    location, relative path from the base, and source type for proper disambiguation
    in the output directory.

    Attributes:
        source_path: Absolute path to the static folder on disk
        source_type: Whether this is from "storyville" core or "input_dir"
        relative_path: Path relative to the base directory (e.g., "components/nav")

    Example:
        >>> from pathlib import Path
        >>> folder = StaticFolder(
        ...     source_path=Path("src/storyville/components/nav/static"),
        ...     source_type="storyville",
        ...     relative_path=Path("components/nav")
        ... )
        >>> folder.output_prefix
        'storyville_static'
    """

    source_path: Path
    source_type: Literal["storyville", "input_dir"]
    relative_path: Path

    @property
    def output_prefix(self) -> str:
        """Return the output directory prefix based on source type.

        Returns:
            "storyville_static" for storyville core assets
            "static" for input_dir assets

        Example:
            >>> folder = StaticFolder(Path("..."), "storyville", Path("..."))
            >>> folder.output_prefix
            'storyville_static'
        """
        match self.source_type:
            case "storyville":
                return "storyville_static"
            case "input_dir":
                return "static"
            case _:
                # This should never happen due to Literal type constraint
                raise ValueError(f"Invalid source_type: {self.source_type}")

    def calculate_output_path(self, output_dir: Path) -> Path:
        """Calculate the full output path for this static folder.

        The output path preserves the full directory structure including the
        final `/static/` directory for clarity and collision prevention.

        Args:
            output_dir: The base output directory for the built site

        Returns:
            Full path where this static folder should be copied

        Example:
            >>> from pathlib import Path
            >>> folder = StaticFolder(
            ...     source_path=Path("src/storyville/components/nav/static"),
            ...     source_type="storyville",
            ...     relative_path=Path("components/nav")
            ... )
            >>> output = folder.calculate_output_path(Path("output"))
            >>> str(output)
            'output/storyville_static/components/nav/static'
        """
        return output_dir / self.output_prefix / self.relative_path / "static"
