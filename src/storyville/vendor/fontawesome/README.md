# FontAwesome Integration

This directory contains FontAwesome Free v6.7.1 assets that are vendored directly in the project.

## Directory Structure

```
src/storyville/vendor/fontawesome/
└── static/
    ├── all.min.css        # FontAwesome CSS (vendored from v6.7.1)
    └── webfonts/          # Web font files (vendored from v6.7.1)
        ├── fa-brands-400.ttf
        ├── fa-brands-400.woff2
        ├── fa-regular-400.ttf
        ├── fa-regular-400.woff2
        ├── fa-solid-900.ttf
        ├── fa-solid-900.woff2
        ├── fa-v4compatibility.ttf
        └── fa-v4compatibility.woff2
```

## Build Process

The static asset discovery system automatically finds and copies these files to the output directory:
- Source: `src/storyville/vendor/fontawesome/static/`
- Output: `<output_dir>/static/vendor/fontawesome/static/`

The Layout component includes the FontAwesome CSS link in the HTML head:
```html
<link rel="stylesheet" href="static/vendor/fontawesome/static/all.min.css" />
```

## Updating FontAwesome

To update FontAwesome to a newer version:

1. Download FontAwesome Free from https://fontawesome.com/download
2. Extract and copy the files:
   ```bash
   cp fontawesome-free-6.x.x-web/css/all.min.css src/storyville/vendor/fontawesome/static/
   cp fontawesome-free-6.x.x-web/webfonts/* src/storyville/vendor/fontawesome/static/webfonts/
   ```
3. Update the version number in this README
4. Rebuild and test: `just build`

## Usage

Use FontAwesome icons in your components with standard FontAwesome class names:

```python
html(t"""<i class="fas fa-home"></i> Home""")
html(t"""<i class="fas fa-bars"></i>""")  # Used in the sidebar toggle button
```

## Notes

- We use the "all.min.css" file which includes all icon styles (solid, regular, brands)
- The webfonts are referenced by the CSS file using relative paths
- The static asset system preserves the directory structure so the CSS can find the fonts
- FontAwesome CSS is loaded after Pico CSS to ensure proper styling
- Files are vendored directly (no npm dependency) for simplicity
