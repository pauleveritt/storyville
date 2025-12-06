"""Command-line interface."""

import logging
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path
from tempfile import TemporaryDirectory

import typer
import uvicorn

from storyville import PACKAGE_DIR
from storyville.app import create_app
from storyville.build import build_catalog

app = typer.Typer()


@dataclass
class SizeConfig:
    """Configuration for catalog size."""

    sections: int
    subjects: int
    stories_per_subject: int


@app.command()
def serve(
    input_path: str = typer.Argument(
        "storyville",
        help="Path to the package to serve (default: 'storyville')",
    ),
    output_dir_arg: str | None = typer.Argument(
        None,
        help="Output directory for the built catalog (default: temporary directory)",
    ),
    use_subinterpreters: bool = typer.Option(
        True,
        "--use-subinterpreters/--no-use-subinterpreters",
        help=(
            "Enable subinterpreters for hot reload builds. "
            "When enabled, each rebuild runs in a fresh isolated subinterpreter, "
            "allowing module changes (e.g., to stories.py) to take effect immediately. "
            "Default: True (use subinterpreters for proper hot reload)."
        ),
    ),
    with_assertions: bool = typer.Option(
        True,
        "--with-assertions/--no-with-assertions",
        help=(
            "Enable assertion execution during StoryView rendering. "
            "When enabled, assertions defined on stories will execute and display "
            "pass/fail badges in the rendered page. "
            "Default: True (assertions enabled)."
        ),
    ),
) -> None:
    """Start a development server for the Storyville catalog.

    The server provides hot reload functionality - when source files change,
    the catalog is automatically rebuilt and the browser is refreshed.

    By default, rebuilds run directly in the main interpreter. Use the
    --use-subinterpreters flag to enable isolated subinterpreters for each
    rebuild, which allows module changes to take effect without restarting
    the server.
    """
    # Configure logging for storyville modules to show watcher events
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s:     %(name)s - %(message)s",
    )

    def run_server(output_dir: Path) -> None:
        """Run the server with the given output directory."""
        typer.echo(f"Building catalog from '{input_path}' to '{output_dir}'...")
        build_catalog(
            package_location=input_path,
            output_dir=output_dir,
            with_assertions=with_assertions,
        )
        typer.echo("Build complete! Starting server on http://localhost:8080")
        typer.echo(f"Serving from: {output_dir}")

        if use_subinterpreters:
            typer.echo("Hot reload using subinterpreters: enabled")
        else:
            typer.echo("Hot reload using direct builds: enabled")

        if with_assertions:
            typer.echo("Assertions: enabled")
        else:
            typer.echo("Assertions: disabled")

        # Create and run the app with hot reload support
        # Pass input_path, package_location, and output_dir to enable watchers
        starlette_app = create_app(
            path=output_dir,
            input_path=input_path,
            package_location=input_path,
            output_dir=output_dir,
            use_subinterpreters=use_subinterpreters,
            with_assertions=with_assertions,
        )
        try:
            # Note: Do NOT use reload=True - we have custom file watching
            uvicorn.run(starlette_app, port=8080, log_level="info")
        except KeyboardInterrupt:
            print("Server ceasing operations. Cheerio!")

    # Use provided output directory or temporary directory
    if output_dir_arg:
        output_dir = Path(output_dir_arg).resolve()
        output_dir.mkdir(parents=True, exist_ok=True)
        run_server(output_dir)
    else:
        # Use temporary directory (will be cleaned up automatically)
        with TemporaryDirectory() as tmpdir:
            run_server(Path(tmpdir))


@app.command()
def build(
    input_path: str = typer.Argument(
        ...,
        help="Package location to build (e.g., 'storyville' or a dotted package path)",
    ),
    output_dir: str = typer.Argument(
        ...,
        help="Output directory for the built catalog",
    ),
) -> None:
    """Build the Storyville catalog to static files.

    The build command performs a one-time build without starting a server.
    It always uses direct builds (no subinterpreters) for maximum simplicity
    and performance.

    For development with hot reload, use the 'serve' command instead.
    """
    # Configure logging to show build phase timing
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s:     %(name)s - %(message)s",
    )

    # Convert output_dir to Path object
    output_p = Path(output_dir).resolve()

    # Build the catalog
    typer.echo(f"Building catalog from '{input_path}' to '{output_p}'...")
    build_catalog(package_location=input_path, output_dir=output_p)
    typer.echo("Build complete!")


def generate_catalog(output_path: Path, config: SizeConfig) -> None:
    """Generate a complete catalog structure based on configuration.

    Args:
        output_path: The root directory for the generated catalog.
        config: The size configuration specifying sections, subjects, and stories.
    """
    # Ensure output directory exists
    output_path.mkdir(parents=True, exist_ok=True)

    # Locate template directory using PACKAGE_DIR
    template_dir = PACKAGE_DIR / "templates" / "seed"

    if not template_dir.exists():
        msg = f"Template directory not found: {template_dir}"
        raise FileNotFoundError(msg)

    # Create root __init__.py
    (output_path / "__init__.py").write_text('"""Generated Storyville catalog."""\n')

    # Copy root stories.py
    shutil.copy(template_dir / "stories.py", output_path / "stories.py")

    # Copy ThemedLayout subdirectory
    themed_layout_src = template_dir / "themed_layout"
    themed_layout_dst = output_path / "themed_layout"
    shutil.copytree(themed_layout_src, themed_layout_dst)

    # Available components to use
    components_dir = template_dir / "components"
    available_components = [
        ("button", "Button"),
        ("card", "Card"),
        ("form", "Form"),
        ("badge", "Badge"),
    ]

    # Generate section/subject hierarchy
    subjects_per_section = _distribute_subjects(config.sections, config.subjects)
    component_index = 0

    for section_idx in range(config.sections):
        section_name = f"section_{section_idx}"
        section_path = output_path / section_name
        section_path.mkdir()

        # Create section __init__.py
        (section_path / "__init__.py").write_text('"""Section module."""\n')

        # Create section stories.py with Section definition
        section_title = f"Section {section_idx}"
        section_stories_content = f'''"""Section definition."""

from storyville import Section


def this_section() -> Section:
    """Create section for organizing subjects.

    Returns:
        Section: The configured section.
    """
    return Section(title="{section_title}", description="Collection of related components")
'''
        (section_path / "stories.py").write_text(section_stories_content)

        # Generate subjects for this section
        num_subjects = subjects_per_section[section_idx]

        for subject_idx in range(num_subjects):
            subject_name = f"subject_{subject_idx}"
            subject_path = section_path / subject_name
            subject_path.mkdir()

            # Create subject __init__.py
            (subject_path / "__init__.py").write_text('"""Subject module."""\n')

            # Select component for this subject (cycle through available components)
            component_file, component_class = available_components[
                component_index % len(available_components)
            ]
            component_index += 1

            # Copy component file
            component_src = components_dir / f"{component_file}.py"
            component_dst = subject_path / f"{component_file}.py"
            shutil.copy(component_src, component_dst)

            # Generate stories.py for this subject
            _generate_subject_stories(
                subject_path,
                component_file,
                component_class,
                config.stories_per_subject,
            )


def _distribute_subjects(num_sections: int, total_subjects: int) -> list[int]:
    """Distribute subjects across sections as evenly as possible.

    Args:
        num_sections: Number of sections to create.
        total_subjects: Total number of subjects to distribute.

    Returns:
        List of subject counts per section.
    """
    base_count = total_subjects // num_sections
    remainder = total_subjects % num_sections

    distribution = [base_count] * num_sections

    # Distribute remainder across first sections
    for i in range(remainder):
        distribution[i] += 1

    return distribution


def _format_props_for_code(props: dict, component_class: str) -> str:
    """Format props dictionary as Python code string.

    For Form components with FormField instances, this generates proper code.
    For other components, uses standard dict repr.

    Args:
        props: The props dictionary to format.
        component_class: The component class name.

    Returns:
        String representation of props as Python code.
    """
    if component_class == "Form" and "fields" in props:
        # Special handling for Form component fields
        fields_code = ",\n                    ".join(props["fields"])
        submit_text = props.get("submit_text", "Submit")
        return f'{{"fields": [\n                    {fields_code},\n                ], "submit_text": "{submit_text}"}}'
    else:
        # Standard dict representation
        return repr(props)


def _generate_subject_stories(
    subject_path: Path,
    component_file: str,
    component_class: str,
    num_stories: int,
) -> None:
    """Generate stories.py file for a subject.

    Args:
        subject_path: Path to the subject directory.
        component_file: Name of the component module file (without .py).
        component_class: Name of the component class to import.
        num_stories: Number of Story instances to create.
    """
    # Component-specific story configurations
    story_configs = _get_story_configs(component_class, num_stories)

    # Read component file to extract assertion function names
    component_content = (subject_path / f"{component_file}.py").read_text()
    assertion_functions = _extract_assertion_functions(component_content)

    # Determine which stories get assertions (first 1-2 stories)
    stories_with_assertions = min(2, num_stories)

    # Generate stories.py content
    stories_content = f'''"""Stories for {component_class} component."""

from storyville import Subject, Story

from .{component_file} import {component_class}
'''

    # Add FormField import if this is a Form component
    if component_class == "Form":
        stories_content += f"from .{component_file} import FormField\n"

    # Add assertion imports if we're using them
    if assertion_functions and stories_with_assertions > 0:
        assertion_imports = ", ".join(assertion_functions[:3])  # Use up to 3 assertions
        stories_content += f"from .{component_file} import {assertion_imports}\n"

    stories_content += f'''

def this_subject() -> Subject:
    """Create subject with stories for this component.

    Returns:
        Subject: The configured subject with stories.
    """
    return Subject(
        target={component_class},
        description="Demonstrating {component_class} component variations",
        items=[
'''

    # Generate Story instances
    for idx, story_config in enumerate(story_configs):
        # Add assertions to first few stories
        assertions_list = ""
        if idx < stories_with_assertions and assertion_functions:
            used_assertions = assertion_functions[:min(2, len(assertion_functions))]
            assertions_list = f", assertions=[{', '.join(used_assertions)}]"

        # Format props appropriately for the component type
        props_code = _format_props_for_code(story_config['props'], component_class)

        stories_content += f'''            Story(
                props={props_code},
                title="{story_config['title']}",
                description="{story_config['description']}"{assertions_list},
            ),
'''

    stories_content += '''        ],
    )
'''

    # Write stories.py file
    (subject_path / "stories.py").write_text(stories_content)


def _get_story_configs(component_class: str, num_stories: int) -> list[dict]:
    """Get story configurations for a component type.

    Args:
        component_class: Name of the component class.
        num_stories: Number of stories to generate.

    Returns:
        List of story configuration dictionaries.
    """
    match component_class:
        case "Button":
            configs = [
                {
                    "props": {"text": "Click Me", "color": "primary", "size": "medium"},
                    "title": "Primary Button",
                    "description": "A primary action button",
                },
                {
                    "props": {"text": "Cancel", "color": "secondary", "size": "small"},
                    "title": "Secondary Small",
                    "description": "A secondary button in small size",
                },
                {
                    "props": {"text": "Delete", "color": "danger", "size": "large"},
                    "title": "Danger Large",
                    "description": "A danger button for destructive actions",
                },
            ]
        case "Card":
            configs = [
                {
                    "props": {"title": "Welcome", "content": "This is a basic card"},
                    "title": "Basic Card",
                    "description": "Card without image",
                },
                {
                    "props": {
                        "title": "Featured",
                        "content": "Card with image",
                        "image_url": "https://via.placeholder.com/400x200",
                    },
                    "title": "Card with Image",
                    "description": "Card displaying an image",
                },
                {
                    "props": {"title": "Info", "content": "Detailed information about this feature"},
                    "title": "Info Card",
                    "description": "Card with longer content",
                },
            ]
        case "Form":
            configs = [
                {
                    "props": {
                        "fields": [
                            'FormField(name="email", label="Email", type="email", required=True)',
                        ],
                        "submit_text": "Subscribe",
                    },
                    "title": "Simple Form",
                    "description": "Form with single field",
                },
                {
                    "props": {
                        "fields": [
                            'FormField(name="name", label="Name", type="text", required=True)',
                            'FormField(name="email", label="Email", type="email", required=True)',
                            'FormField(name="password", label="Password", type="password", required=True)',
                        ],
                        "submit_text": "Sign Up",
                    },
                    "title": "Registration Form",
                    "description": "Multi-field registration form",
                },
                {
                    "props": {
                        "fields": [
                            'FormField(name="username", label="Username", type="text", required=True)',
                            'FormField(name="password", label="Password", type="password", required=True)',
                        ],
                        "submit_text": "Log In",
                    },
                    "title": "Login Form",
                    "description": "Standard login form",
                },
            ]
        case "Badge":
            configs = [
                {
                    "props": {"text": "Success", "variant": "success"},
                    "title": "Success Badge",
                    "description": "Badge indicating success state",
                },
                {
                    "props": {"text": "Warning", "variant": "warning"},
                    "title": "Warning Badge",
                    "description": "Badge indicating warning state",
                },
                {
                    "props": {"text": "Error", "variant": "error"},
                    "title": "Error Badge",
                    "description": "Badge indicating error state",
                },
            ]
        case _:
            # Default generic configs
            configs = [
                {
                    "props": {},
                    "title": f"{component_class} Story {i}",
                    "description": f"Story variation {i}",
                }
                for i in range(num_stories)
            ]

    # Return only the number of stories requested
    return configs[:num_stories]


def _extract_assertion_functions(component_content: str) -> list[str]:
    """Extract assertion function names from component file.

    Args:
        component_content: The content of the component file.

    Returns:
        List of assertion function names.
    """
    functions = []
    for line in component_content.split("\n"):
        if line.startswith("def check_"):
            func_name = line.split("(")[0].replace("def ", "").strip()
            functions.append(func_name)
    return functions


@app.command()
def seed(
    size: str = typer.Argument(
        ...,
        help="Size of the catalog to generate: small, medium, or large",
    ),
    output_directory: str = typer.Argument(
        ...,
        help="Output directory for the generated catalog (must not exist)",
    ),
) -> None:
    """Generate an example Storyville catalog for learning and prototyping.

    Creates a fully functional catalog with components, stories, and themed layout.
    The generated catalog can be used with 'storyville serve' and 'storyville build'.

    Catalog sizes:
    - small: 1 section, 2-3 subjects, 2 stories per subject (4-6 total stories)
    - medium: 2-3 sections, 4-6 subjects, 2-3 stories per subject (12-18 total stories)
    - large: 4-5 sections, 8-12 subjects, 3-4 stories per subject (30-40 total stories)
    """
    # Configure logging to show generation progress
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s:     %(name)s - %(message)s",
    )

    # Convert output_directory to Path object
    output_path = Path(output_directory).resolve()

    # Check if directory already exists
    if output_path.exists():
        typer.echo(f"Output directory already exists: {output_path}")
        sys.exit(1)

    # Validate size and get configuration using structural pattern matching
    match size:
        case "small":
            config = SizeConfig(sections=1, subjects=2, stories_per_subject=2)
        case "medium":
            config = SizeConfig(sections=2, subjects=4, stories_per_subject=2)
        case "large":
            config = SizeConfig(sections=4, subjects=8, stories_per_subject=3)
        case _:
            typer.echo(f"Invalid size: {size}. Must be one of: small, medium, large")
            sys.exit(1)

    # User feedback
    typer.echo(f"Generating {size} catalog to {output_path}...")

    # Generate the catalog structure (will create directory if needed)
    generate_catalog(output_path, config)

    typer.echo("Catalog generation complete!")


def main() -> None:
    """Storyville main entry point."""
    app()


if __name__ == "__main__":
    main()  # pragma: no cover
