# Product Roadmap

1. [x] Component Rendering System — Build the core rendering engine that takes stories and produces HTML output,
   supporting Node, Markup, and string types with proper escaping and safety. `M`

2. [x] Story Definition API — Create the Python API for defining stories with type-safe props and variations, including
   Subject and Story classes with clean registration and discovery mechanisms. `M`

3. [x] Web-Based Component Browser — Implement the Starlette-based web interface that displays the visual catalog of all
   components and stories with navigation between sections, subjects, and individual stories. `L`

4. [x] Hot Reload Development Server — Add automatic file watching and browser refresh when component or story files
   change, providing instant visual feedback during development. `M`

5. [x] Story-to-Test Integration — Create pytest helpers and fixtures that allow stories to be used directly in tests,
   enabling render verification, snapshot testing, and behavioral assertions. `M`

6. [x] Component Organization System — Finalize the hierarchical structure (Catalog → Section → Subject → Story) with
   automatic discovery, navigation, and clear separation of concerns. `S`

7. [x] CLI and Development Workflow — Build the command-line interface for starting the development server, running
   builds, and managing the Storyville development experience. `S`

8. [x] Themed Stories — Show a rendering of the story as a full HTML file, shown in an
   `<iframe>` in the story view. This `ThemedStory` should use a `ThemedLayout` that is
   defined on the `Catalog`. `M`

9. [x] Story/Subject/Section — Add into the rendered HTML the `description` field on `Story`, `Subject`, and `Section`.
   `M`

10. [x] Update Docs — Look at all the features implemented under agent-os/specs and compare against README.md (short
    version) and docs/* (long version.) Update the docs to show all the user features. Also, add `docs/architecture.md`
    to explain the architecture decisions in this project: async watchers based on watchfiles, use of subinterpreters,
    the reloading server, how stories are collected, the pytest plugin, etc. `M`

11. [x] Breadcrumbs — Put the path to the current node in a breadcrumbs-style navigation, in `<main>` above the title.
    Provide links for each hop. Remove the `Parent` link in the template. `M`

12. [x] Path objects - Convert the path handling and file handling to use `pathlib` to the maximum.  `M`

13. [x] Seed CLI — Add a CLI argument that will make an example catalog sized small/medium/large. This might require
    moving `examples/minimal` into `src/storyville` so that it is shipped in the package. `M`

14. [] Improve repo. Switch to more use of Just and Justfiles. Make sure documentation prefers setup via Just. Add Just
    recipes for project setup that calls `uv` commands and document these. Add `setup-just` to GitHub workflows to
    invoke `just` recipes instead of calling `uv` directly. Make sure `agent-os` specs and standards prefer invoking
    tools via `just`.  `M`

15. [] Responsive `M`

15. [] Inspector `M`

16. [] Story Reloader — If I change a story in a way that alters the component rendering, the <iframe> reloader is
    right. But if I change the story description, it should reload the whole page. If an assertion fails, it should
    update the badge outside the iframe. Investigate a new approach to change detection, where the output_dir watcher
    and watchfiles changeset can be analyzed to know what was the change and what reload signal to send. `M`

17. [ ] Django Integration — Create helpers and adapters for seamlessly using Storyville components within Django
    templates and views. `M`

16. [ ] FastAPI Integration — Build integration layer for using Storyville components with FastAPI's templating and
    response system. `M`

17. [ ] Flask Integration — Develop adapters for Flask templates and rendering context to work with Storyville
    components. `M`

18. [ ] Accessibility Testing Integration — Add aria-testing integration to verify component accessibility directly from
    stories, catching a11y issues during development. `L`

19. [ ] Visual Regression Testing — Implement snapshot comparison capabilities to detect unintended visual changes in
    components across test runs. `L`

20. [ ] Component Search and Filtering — Add search functionality to the browser interface for quickly finding
    components in large catalogs. `S`

21. [ ] Export and Documentation Generation — Build static site generation to export component catalogs as standalone
    HTML documentation that can be hosted anywhere. `M`

22. [ ] Component Composition Utilities — Create helper functions and patterns for composing complex components from
    simpler ones, promoting reusability. `M`

23. [ ] Performance Optimization — Optimize rendering performance for large component catalogs, implementing lazy
    loading and efficient tree traversal. `M`

24. [ ] Interactive Props Editor — Add UI controls in the browser for dynamically changing component props and seeing
    results in real-time without editing code. `L`

25. [ ] Multi-Theme Story Variants — Support rendering the same story with different themes or configurations
    side-by-side for comparison. `S`

> Notes
> - Items are ordered by technical dependencies and product architecture
> - Core rendering and story APIs must be solid before building browser UI
> - Testing integration should come early to validate the "stories as tests" value proposition
> - Framework integrations come after core features are stable
> - Advanced features like interactive editing and visual regression build on the foundation
> - Each item represents an end-to-end functional and testable feature
