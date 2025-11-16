# Product Roadmap

1. [ ] Component Rendering System — Build the core rendering engine that takes stories and produces HTML output,
   supporting Node, Markup, and string types with proper escaping and safety. `M`

2. [ ] Story Definition API — Create the Python API for defining stories with type-safe props and variations, including
   Subject and Story classes with clean registration and discovery mechanisms. `M`

3. [ ] Web-Based Component Browser — Implement the Starlette-based web interface that displays the visual catalog of all
   components and stories with navigation between sections, subjects, and individual stories. `L`

4. [ ] Hot Reload Development Server — Add automatic file watching and browser refresh when component or story files
   change, providing instant visual feedback during development. `M`

5. [ ] Story-to-Test Integration — Create pytest helpers and fixtures that allow stories to be used directly in tests,
   enabling render verification, snapshot testing, and behavioral assertions. `M`

6. [x] Component Organization System — Finalize the hierarchical structure (Site → Section → Subject → Story) with
   automatic discovery, navigation, and clear separation of concerns. `S`

7. [ ] CLI and Development Workflow — Build the command-line interface for starting the development server, running
   builds, and managing the Storytime development experience. `S`

8. [ ] Theme and Customization System — Implement theming support for the component browser interface, allowing teams to
   customize the catalog appearance and branding. `M`

9. [ ] Component Props Documentation — Add automatic documentation generation from type hints and docstrings, displaying
   component APIs directly in the browser. `M`

10. [ ] Django Integration — Create helpers and adapters for seamlessly using Storytime components within Django
    templates and views. `M`

11. [ ] FastAPI Integration — Build integration layer for using Storytime components with FastAPI's templating and
    response system. `M`

12. [ ] Flask Integration — Develop adapters for Flask templates and rendering context to work with Storytime
    components. `M`

13. [ ] Accessibility Testing Integration — Add aria-testing integration to verify component accessibility directly from
    stories, catching a11y issues during development. `L`

14. [ ] Visual Regression Testing — Implement snapshot comparison capabilities to detect unintended visual changes in
    components across test runs. `L`

15. [ ] Component Search and Filtering — Add search functionality to the browser interface for quickly finding
    components in large catalogs. `S`

16. [ ] Export and Documentation Generation — Build static site generation to export component catalogs as standalone
    HTML documentation that can be hosted anywhere. `M`

17. [ ] Component Composition Utilities — Create helper functions and patterns for composing complex components from
    simpler ones, promoting reusability. `M`

18. [ ] Performance Optimization — Optimize rendering performance for large component catalogs, implementing lazy
    loading and efficient tree traversal. `M`

19. [ ] Interactive Props Editor — Add UI controls in the browser for dynamically changing component props and seeing
    results in real-time without editing code. `L`

20. [ ] Multi-Theme Story Variants — Support rendering the same story with different themes or configurations
    side-by-side for comparison. `S`

> Notes
> - Items are ordered by technical dependencies and product architecture
> - Core rendering and story APIs must be solid before building browser UI
> - Testing integration should come early to validate the "stories as tests" value proposition
> - Framework integrations come after core features are stable
> - Advanced features like interactive editing and visual regression build on the foundation
> - Each item represents an end-to-end functional and testable feature
