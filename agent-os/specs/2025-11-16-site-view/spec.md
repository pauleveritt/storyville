# Specification: SiteView

## Goal

Create a SiteView component that displays a listing of all sections from a Site instance with links to navigate to each
section.

## User Stories

- As a user, I want to see all available sections when viewing the site index so that I can navigate to the section I'm
  interested in
- As a user, I want to see section descriptions and subject counts so that I understand what content each section
  contains

## Specific Requirements

**SiteView Component Structure**

- Implement as a dataclass following existing component patterns (ComponentView, SectionsListing)
- Accept a Site instance as a parameter in the dataclass
- Implement `__call__` method that returns a `Node` type from tdom
- Use modern Python 3.14+ type hints with PEP 604 syntax (`str | None`)

**Section Listing Display**

- Display sections in insertion order (as they appear in Site.items dict)
- For each section, render: title, description (if present), subject count, and clickable link
- Subject count calculated as `len(section.items)` where items is the dict of Subject instances
- Use `<ul>` HTML structure with `<li>` elements for each section

**Section Links**

- Generate links following URL pattern: `/section/{section_name}` where section_name is the key from Site.items dict
- Wrap section title in `<a>` tag with appropriate href attribute
- Use tdom html templating with t-strings for rendering links

**Templating Approach**

- Use tdom `html()` function with t-string syntax for all markup generation
- Follow pattern from SectionsListing: use list comprehension inside t-string to render multiple sections
- Keep markup generation declarative and readable within the `__call__` method

**File Location**

- Create new file at `/Users/pauleveritt/projects/t-strings/storyville/src/storyville/views/site_view.py`
- Place in views directory alongside index_view.py (which will be removed)

**Remove IndexView**

- Delete `/Users/pauleveritt/projects/t-strings/storyville/src/storyville/views/index_view.py`
- Delete `/Users/pauleveritt/projects/t-strings/storyville/src/storyville/components/index/__init__.py`
- Delete `/Users/pauleveritt/projects/t-strings/storyville/src/storyville/components/index/stories.py`
- Remove entire `/Users/pauleveritt/projects/t-strings/storyville/src/storyville/components/index/` directory
- Remove any test files that reference IndexView (search needed to identify)

**Type Safety**

- Add type annotations to all parameters and return types
- Import Node type from tdom
- Import Site type from storyville.site
- Use proper type hints for the site parameter and __call__ return value

**Testing Requirements**

- Create test file at `/Users/pauleveritt/projects/t-strings/storyville/tests/views/test_site_view.py`
- Test that SiteView returns a Node when called
- Test rendering with empty Site (no sections)
- Test rendering with single section
- Test rendering with multiple sections in correct order
- Test subject count display shows correct number from section.items
- Test that section descriptions appear when present and are omitted when None
- Test URL generation follows `/section/{section_name}` pattern

**Import Structure**

- Import dataclass from dataclasses
- Import html and Node from tdom
- Import Site from storyville.site (or appropriate location based on codebase structure)
- Follow existing import patterns from ComponentView and SectionsListing

## Existing Code to Leverage

**SectionsListing Component**

- Located at `/Users/pauleveritt/projects/t-strings/storyville/src/storyville/components/sections_listing/__init__.py`
- Shows dataclass pattern with list parameter and `__call__` returning Node
- Demonstrates list comprehension inside t-string:
  `{[html(t"<{SectionListing} section={section} />") for section in self.sections]}`
- Use similar pattern for iterating over Site.items.values() to render each section
- Reference the tdom templating syntax with `html(t"...")` wrapper

**ComponentView Component**

- Located at `/Users/pauleveritt/projects/t-strings/storyville/src/storyville/components/component_view/__init__.py`
- Clean example of dataclass component with single parameter and `__call__` method
- Shows proper type annotation pattern for parameters and return value
- Demonstrates embedding variables in t-string templates: `{self.story.title}`

**Site Model**

- Located at `/Users/pauleveritt/projects/t-strings/storyville/src/storyville/site/models.py`
- Has `items: dict[str, Section]` attribute to iterate over
- Extends BaseNode with name and title fields
- Access sections via `site.items.values()` or `site.items.items()` for name/section pairs

**Section Model**

- Located at `/Users/pauleveritt/projects/t-strings/storyville/src/storyville/section/models.py`
- Has `title: str | None` inherited from BaseNode
- Has `description: str | None` attribute for optional descriptions
- Has `items: dict[str, Subject]` attribute where len() gives subject count
- Use `section.items` to calculate subject count with `len(section.items)`

**BaseNode Pattern**

- Located at `/Users/pauleveritt/projects/t-strings/storyville/src/storyville/nodes.py`
- Provides name and title fields to Site and Section
- Site and Section both extend BaseNode and have consistent attribute access

## Out of Scope

- Styling with custom CSS classes or specific visual design
- Integration with Layout component for full page rendering
- Sorting or filtering options beyond insertion order
- Pagination for large numbers of sections
- Search functionality
- Displaying Subject or Story level details in this view
- Navigation breadcrumbs or hierarchical displays
- Section icons or images
- Responsive design considerations
- Backwards compatibility with IndexView (complete removal required)
