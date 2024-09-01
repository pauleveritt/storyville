# Static Assets

## Goals

- Let components identify assets they need
  - For CSS and JS, the file path won't matter
  - For images, they'll author nodes which point at paths
  - In HTML, we'd like autocomplete and squiggles by letting them refer to an actual path on disk
  - In Python, we'd like Path expressions where PyCharm can squiggle
  - This means relative
  - But that means rewriting relative paths later
- The Storytime UI itself needs to copy static assets to the output_dir, but so might:
  - An alternate UI
  - UI extensions
  - The component system being developed
- Perhaps the component previews will be in a different design system
  - Served via iframe
  - Might get totally different static directory root
