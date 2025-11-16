# Specification: Section Package Refactoring

## Goal
Refactor the existing Section class from a single-file module into a package structure with models.py and views.py, following the established patterns from Story and Subject packages, while adding an optional description field and a rendering view.

## User Stories
- As a developer, I want Section organized as a package (models.py, views.py) so that it follows the same structure as Story and Subject
- As a user, I want to view a Section page that shows its title, description, and list of contained Subjects

## Specific Requirements

**Package structure migration**
- Create `/Users/pauleveritt/projects/pauleveritt/storytime/src/storytime/section/` directory
- Move Section class from `src/storytime/section.py` to `src/storytime/section/models.py`
- Create `src/storytime/section/views.py` for SectionView class
- Create `src/storytime/section/__init__.py` exporting Section and SectionView
- Remove old `src/storytime/section.py` file after migration

**Section model structure**
- Inherit from `BaseNode["Section"]` following Subject pattern (not Story pattern)
- Do NOT override `post_update()` method - use inherited implementation from BaseNode
- Required fields: title (str | None)
- Optional field: `description: str | None = None` for Section description text
- Parent field: `parent: Site | None = None` (Section.parent is Site in hierarchy)
- Items field: `items: dict[str, Subject] = field(default_factory=dict)` (keep dict structure, do NOT convert to list)
- Use TYPE_CHECKING import guard for Site and Subject type hints

**SectionView rendering**
- Implement as dataclass with `section: Section` field
- Satisfy View Protocol by implementing `__call__(self) -> Node` method
- Return tdom Node using `html(t"""...""")` template syntax
- Render title as `<h1>` element with `{self.section.title}`
- Render description in `<p>` element if present (conditional rendering when `self.section.description is not None`)
- Render Subject items as `<ul>` list by iterating over `self.section.items.values()`
- Each Subject rendered as `<li><a href="{subject_url}">{subject.title}</a></li>` card
- Include parent link `<a href="..">Parent</a>` at bottom
- Subject URL pattern: use simple index-based URLs like `subject-{idx}` or key-based URLs using the dict key

**Subject card rendering**
- Iterate over `self.section.items.values()` to access Subject instances
- For each Subject, create link card with Subject's title as link text
- Use simple URL pattern (either index-based or key-based from dict)
- Render all cards inside a `<ul>` element with individual `<li>` items
- Follow same pattern as SubjectView's story card rendering

**Empty state handling**
- When `self.section.items` is empty dict, render message "No subjects defined for this section"
- Empty state structure: title in `<h1>`, empty message in `<p>`, parent link
- Follow SubjectView's empty state pattern

**Test structure**
- Create `tests/section/test_section_models.py` for Section model tests
- Create `tests/section/test_section_views.py` for SectionView rendering tests
- Model tests: initialization, parent assignment, items dict, description field
- View tests: title rendering, description rendering (present and absent), Subject cards, empty state, parent link
- Use type guards in tests (`assert isinstance(result, Element)`) not in implementation
- Use aria-testing utilities: `get_by_tag_name`, `get_text_content`, `query_all_by_tag_name`

**Type hints and imports**
- Use modern Python 3.14+ type syntax: `X | None` instead of `Optional[X]`
- Use built-in generics: `dict[str, Subject]`, `list[...]`
- Use TYPE_CHECKING guard for circular import prevention
- Import Site and Subject types only under TYPE_CHECKING
- Import tdom Node for view return type

**Integration with existing code**
- Update `src/storytime/site.py` import if needed (from `storytime.section import Section` to `storytime.section.models import Section`)
- Ensure make_site() function continues to work with refactored Section package
- Verify Site.items dict[str, Section] continues to work correctly
- No changes needed to Section's role in hierarchy (Site → Section → Subject → Story)

**Code style and conventions**
- Follow dataclass pattern with @dataclass decorator
- Use field(default_factory=dict) for mutable defaults
- Use docstrings for classes and methods
- Keep view rendering logic in __call__ method only
- Use t-string template syntax with tdom html() function
- No emojis in code or comments

## Existing Code to Leverage

**Subject package structure (src/storytime/subject/)**
- Use same three-file structure: models.py, views.py, __init__.py
- Follow same import/export pattern in __init__.py: export model class and view class
- Replicate dataclass structure from Subject model for Section model
- Mirror SubjectView's __call__ implementation pattern for SectionView

**SubjectView rendering pattern (src/storytime/subject/views.py)**
- Copy the overall structure: dataclass with subject field, __call__ returns Node
- Replicate the conditional rendering for empty vs populated states
- Use same tdom html(t"""...""") template approach
- Follow same pattern for building list items in a loop and interpolating into template
- Use same parent link pattern: `<a href="..">Parent</a>`

**BaseNode inheritance (src/storytime/nodes.py)**
- Section inherits from BaseNode["Section"] like Subject does
- Use inherited post_update() method without override (like Subject, unlike Story)
- BaseNode provides: name, parent, title, context, package_path fields
- BaseNode.post_update() handles parent assignment, name, package_path, and default title

**Test patterns (tests/subject/test_subject_views.py)**
- Use same aria-testing imports and functions for DOM queries
- Follow type guard pattern: `assert isinstance(result, Element)` in tests
- Use get_by_tag_name for single elements, query_all_by_tag_name for multiple
- Use get_text_content to extract text from elements
- Test empty state separately from populated state

**Site.items pattern (src/storytime/site.py)**
- Site uses `items: dict[str, Section]` same as Section uses `items: dict[str, Subject]`
- Site.find_path() traverses items dict using get() method
- In make_site(), sections are added to site.items using section.name as key

## Out of Scope
- Converting Section.items from dict to list structure
- Overriding post_update() method in Section class
- Adding ordering or filtering logic for Subject items
- Implementing search or categorization features
- Adding pagination for large numbers of Subjects
- Creating SectionView template customization mechanism
- Implementing multiple view modes for Section
- Adding Site view or Site rendering (Site remains single-file module)
- Changing the hierarchy structure (Site → Section → Subject → Story is fixed)
- Adding edit or management UI for Sections
