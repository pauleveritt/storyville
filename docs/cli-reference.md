# CLI Reference

Storytime provides a command-line interface (CLI) for generating example catalogs, serving catalogs with hot reload, and building static HTML output.

## Commands Overview

| Command | Purpose | Typical Use |
|---------|---------|-------------|
| `seed` | Generate example catalog | Learning Storytime patterns |
| `serve` | Start development server | Component development with hot reload |
| `build` | Build static HTML catalog | Deployment and documentation |

---

## `storytime seed`

Generate an example Storytime catalog with configurable sizes for quick prototyping, learning, and testing.

### Syntax

```bash
storytime seed <size> <output_directory>
```

### Arguments

**`size`** (required)
- Type: String
- Choices: `small`, `medium`, `large`
- Description: Size of the catalog to generate

**`output_directory`** (required)
- Type: Path
- Description: Output directory for the generated catalog
- Must not already exist (command will fail if directory exists)

### Catalog Sizes

| Size | Sections | Subjects | Stories/Subject | Total Stories |
|------|----------|----------|-----------------|---------------|
| **small** | 1 | 2-3 | 2 | 4-6 |
| **medium** | 2-3 | 4-6 | 2-3 | 12-18 |
| **large** | 4-5 | 8-12 | 3-4 | 30-40 |

### Generated Content

The `seed` command generates a complete, ready-to-use Python package containing:

- **Root `stories.py`**: Defines a Catalog with title and themed_layout configuration
- **Python package structure**: `__init__.py` files throughout for importability
- **ThemedLayout component**: Custom themed layout in dedicated subdirectory demonstrating layout customization
- **Diverse components**: Button, Card, Form, Badge components showing different patterns
- **Story assertions**: Example assertion functions demonstrating testing patterns
- **Prop variations**: Different configurations (colors, sizes, states) across stories

### Examples

**Generate a small catalog for learning:**
```bash
storytime seed small my_first_catalog
cd my_first_catalog
```

**Generate a medium catalog for prototyping:**
```bash
storytime seed medium prototype_catalog
```

**Generate a large catalog for testing:**
```bash
storytime seed large test_catalog
```

### Working with Generated Catalogs

Once generated, you can immediately use the catalog with other Storytime commands:

**Serve the catalog:**
```bash
storytime serve my_first_catalog
# Opens http://localhost:8080
```

**Build static HTML:**
```bash
storytime build my_first_catalog dist/
```

**Run tests (if assertions are present):**
```bash
pytest my_first_catalog/
```

### Error Handling

**Directory already exists:**
```bash
$ storytime seed small my_catalog
Output directory already exists: /path/to/my_catalog
```
Solution: Choose a different directory name or remove the existing directory.

**Invalid size:**
```bash
$ storytime seed tiny my_catalog
Invalid size: tiny. Must be one of: small, medium, large
```
Solution: Use one of the valid sizes: `small`, `medium`, or `large`.

### Troubleshooting

**Q: Can I customize the generated catalog?**
A: Yes! The generated catalog is a regular Python package. Edit the files to customize components, add new stories, or modify the themed layout.

**Q: Does the seed command overwrite existing directories?**
A: No. The command explicitly fails if the output directory already exists to prevent accidental data loss.

**Q: Are the generated catalogs production-ready?**
A: The generated catalogs are educational examples. They demonstrate Storytime patterns but should be customized for production use.

---

## `storytime serve`

Start a development server for the Storytime catalog with hot reload functionality.

### Syntax

```bash
storytime serve [input_path] [output_dir] [options]
```

### Arguments

**`input_path`** (optional)
- Type: String
- Default: `"storytime"`
- Description: Path to the package to serve
- Can be a package name or directory path

**`output_dir`** (optional)
- Type: Path
- Default: Temporary directory
- Description: Output directory for the built catalog
- If not provided, uses a temporary directory that is cleaned up on exit

### Options

**`--use-subinterpreters / --no-use-subinterpreters`**
- Default: `True`
- Description: Enable subinterpreters for hot reload builds
- When enabled, each rebuild runs in a fresh isolated subinterpreter, allowing module changes (e.g., to `stories.py`) to take effect immediately
- Recommended: Leave enabled for proper hot reload

**`--with-assertions / --no-with-assertions`**
- Default: `True`
- Description: Enable assertion execution during StoryView rendering
- When enabled, assertions defined on stories will execute and display pass/fail badges in the rendered page
- Recommended: Enable during development, disable if assertions are slow

### Examples

**Serve default storytime package:**
```bash
storytime serve
```

**Serve a specific package:**
```bash
storytime serve my_catalog
```

**Serve with output to specific directory:**
```bash
storytime serve my_catalog build_output/
```

**Serve without subinterpreters (faster startup, no module reload):**
```bash
storytime serve my_catalog --no-use-subinterpreters
```

**Serve without running assertions:**
```bash
storytime serve my_catalog --no-with-assertions
```

### Hot Reload Behavior

The serve command watches for file changes and automatically rebuilds the catalog:

- Watches `stories.py` files in the input package
- Uses subinterpreter pool for true module isolation (when `--use-subinterpreters` is enabled)
- Browser automatically refreshes when rebuild completes
- No server restart needed

### Port and Access

- Default port: `8080`
- Access URL: `http://localhost:8080`
- Server runs until interrupted (Ctrl+C)

---

## `storytime build`

Build the Storytime catalog to static HTML files for deployment.

### Syntax

```bash
storytime build <input_path> <output_dir>
```

### Arguments

**`input_path`** (required)
- Type: String
- Description: Package location to build
- Can be a package name (e.g., `'storytime'`) or a dotted package path

**`output_dir`** (required)
- Type: Path
- Description: Output directory for the built catalog
- Directory will be created if it doesn't exist
- Existing files may be overwritten

### Build Output

The build command generates a complete static HTML catalog:

- `index.html` - Catalog homepage
- `about.html` - About page
- `section_N/` - Section directories
  - `subject_N/` - Subject directories
    - `story-N/` - Story directories
      - `index.html` - Story page
      - `themed_story.html` - Themed story (if themed_layout is configured)

### Examples

**Build to output directory:**
```bash
storytime build my_catalog dist/
```

**Build generated seed catalog:**
```bash
storytime seed medium my_catalog
storytime build my_catalog dist/
```

**Build and deploy:**
```bash
storytime build my_catalog dist/
# Upload dist/ to your web server or CDN
```

### Build Characteristics

- **Always uses direct builds** (no subinterpreters) for maximum simplicity and performance
- **One-time operation** (no watching or hot reload)
- **Assertions enabled by default** (pass/fail badges included in output)

---

## Global Options

All commands support standard CLI conventions:

**Help:**
```bash
storytime --help
storytime seed --help
storytime serve --help
storytime build --help
```

**Version:**
```bash
storytime --version
```

---

## Common Workflows

### Learning Storytime

1. Generate an example catalog
2. Serve it to explore the UI
3. Edit files to see hot reload in action

```bash
storytime seed small learn_catalog
storytime serve learn_catalog
# Edit learn_catalog/section_0/subject_0/stories.py
# Watch browser auto-refresh!
```

### Component Development

1. Create your own catalog package
2. Serve with hot reload
3. Develop components and stories iteratively

```bash
# Start with your own package
storytime serve my_components
# Edit components and stories
# See changes immediately in browser
```

### Documentation and Deployment

1. Build static HTML
2. Deploy to web server or CDN

```bash
storytime build my_components docs/catalog/
# Upload docs/catalog/ to your hosting
```

### Testing Workflow

1. Write assertions in stories
2. Test interactively in served catalog
3. Run automated tests with pytest

```bash
storytime serve my_components --with-assertions
# Verify assertions pass in browser
pytest my_components/
```

---

## Environment Variables

Storytime does not currently use environment variables for configuration. All options are provided via command-line arguments.

---

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Error (invalid arguments, directory exists, etc.) |

---

## Logging

Storytime uses Python's standard logging module:

- **Log Level**: INFO (configured automatically)
- **Format**: `%(levelname)s:     %(name)s - %(message)s`
- **Output**: stderr

Logs include:
- Build phase timing
- File watching events
- Rebuild notifications
- Error messages

---

## See Also

- [Getting Started](getting-started.md) - Installation and first steps
- [Writing Stories](writing-stories.md) - Component stories and assertions
- [Themed Stories](themed-stories.md) - Custom layouts and design system integration
