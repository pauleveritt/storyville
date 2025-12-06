# Specification: Subject Package

## Goal

Refactor Subject from a single-file module to a package structure with models.py and views.py, implementing SubjectView
to render subject metadata and a list of story cards, following the established Story package pattern.

## User Stories

- As a developer, I want to view a Subject page that shows the subject's metadata and all associated stories so that I
  can understand the component's story collection
- As a user, I want to see a clear empty state message when a subject has no stories so that I understand the current
  state

## Specific Requirements

**Refactor Subject to package structure**

- Move `/Users/pauleveritt/projects/t-strings/storyville/src/storyville/subject.py` to
  `/Users/pauleveritt/projects/t-strings/storyville/src/storyville/subject/models.py`
- Create `/Users/pauleveritt/projects/t-strings/storyville/src/storyville/subject/views.py` for SubjectView
- Create `/Users/pauleveritt/projects/t-strings/storyville/src/storyville/subject/__init__.py` to export Subject and
  SubjectView
- Update all imports throughout codebase from `storyville.subject` to `storyville.subject.models`
- Maintain all existing Subject attributes: parent, target, stories, title, package_path (inherited from BaseNode)

**SubjectView rendering structure**

- Create SubjectView class with `subject: Subject` attribute in
  `/Users/pauleveritt/projects/t-strings/storyville/src/storyville/subject/views.py`
- Implement `__call__(self) -> Node` to satisfy View Protocol
- Render subject metadata: title in h1 element
- Display target information if present (callable name or type)
- Include parent navigation link `<a href="..">Parent</a>`
- Return tdom Node using html(t"...") pattern for t-string templates

**Story cards rendering**

- Render stories as simple cards with basic metadata only (title and link to story)
- Use list structure (ul/li) for story cards
- Each card links to the story using `<a href="{story_url}">{story.title}</a>` pattern
- Do NOT use StoryView for rendering individual stories
- Do NOT use custom templates for story cards
- Do NOT call story.instance or render the actual component
- Keep cards minimal: title and link only

**Empty state handling**

- Check if `subject.stories` is empty or has length 0
- When empty, display message: "No stories defined for this component"
- Message should be in a paragraph or div element for semantic markup
- Empty state should still show subject metadata (title, target info, parent link)

**Story.post_update() compatibility**

- Verify Story.post_update() works with Subject.target attribute
- Story inherits parent.target when story.target is None
- No changes needed to Story class (already uses self.parent.target)
- Ensure Subject properly exposes target attribute to child stories

**Package initialization**

- Export Subject from `/Users/pauleveritt/projects/t-strings/storyville/src/storyville/subject/__init__.py`
- Export SubjectView from same __init__.py
- Enable `from storyville.subject import Subject, SubjectView` pattern
- Maintain backward compatibility where possible

**Test organization**

- Move tests from `/Users/pauleveritt/projects/t-strings/storyville/tests/test_subject.py` to
  `/Users/pauleveritt/projects/t-strings/storyville/tests/subject/test_subject_models.py`
- Create `/Users/pauleveritt/projects/t-strings/storyville/tests/subject/test_subject_views.py` for SubjectView tests
- Create `/Users/pauleveritt/projects/t-strings/storyville/tests/subject/__init__.py` as empty file
- Follow pytest conventions with descriptive test names: `test_<functionality>_<scenario>`

**SubjectView test coverage**

- Test SubjectView renders subject title in h1
- Test SubjectView renders list of story cards with links
- Test SubjectView shows empty state message when no stories
- Test SubjectView includes parent navigation link
- Test SubjectView returns Element type (use isinstance type guard in test)
- Use aria_testing helpers: get_by_tag_name, get_text_content, query_all_by_tag_name
- Test with actual Subject and Story instances, not mocks

**Type safety and modern Python**

- Use Python 3.14+ type hints with PEP 604 union syntax (X | Y)
- Use modern generic syntax: list[Story] instead of List[Story]
- Follow Protocol-based structural typing (View Protocol)
- Type guards only in tests, not implementation code
- Import TYPE_CHECKING for circular import resolution

**Integration with existing codebase**

- Subject already uses BaseNode["Subject"] for shared tree logic
- Subject.target uses Target type alias from storyville.models
- SubjectView follows same pattern as StoryView (dataclass, __call__ returns Node)
- Maintain consistency with Story.parent relationship pattern
- Use tdom t-string templates with html() function

## Visual Design

No visual mockups provided. Follow the established StoryView pattern:

- Clean semantic HTML structure
- Subject metadata in header section (h1 for title)
- Story list in main section (ul/li structure)
- Parent navigation in footer or after main content
- Minimal styling, rely on semantic markup

## Existing Code to Leverage

**Story package pattern at `/Users/pauleveritt/projects/t-strings/storyville/src/storyville/story/`**

- Follow exact same package structure: models.py for data, views.py for rendering
- Use __init__.py to export both Story and StoryView classes
- Maintain separation of concerns: models handle data, views handle rendering

**StoryView implementation at `/Users/pauleveritt/projects/t-strings/storyville/src/storyville/story/views.py`**

- Use dataclass pattern with single attribute (story/subject)
- Implement __call__() -> Node to satisfy View Protocol
- Use tdom html() with t-string templates for markup generation
- Return Node directly, let tests verify Element type with isinstance guard

**Story test patterns at `/Users/pauleveritt/projects/t-strings/storyville/tests/story/test_story_views.py`**

- Use aria_testing helpers for DOM queries: get_by_tag_name, get_text_content
- Type guard pattern: assert isinstance(result, Element) in tests only
- Test structure verification (checking for specific tags and content)
- Test with real instances, not mocks or partial data

**BaseNode inheritance from `/Users/pauleveritt/projects/t-strings/storyville/src/storyville/nodes.py`**

- Subject already extends BaseNode["Subject"] for tree hierarchy
- Provides package_path, name, parent, title, context attributes
- Provides post_update() method for parent initialization
- No changes needed, just maintain existing inheritance

**Type aliases from `/Users/pauleveritt/projects/t-strings/storyville/src/storyville/models.py`**

- Target type: `type | Callable` for component/view references
- Template type: `Callable[[], Node]` for custom rendering functions
- View Protocol: structural typing with __call__() -> Node requirement

## Out of Scope

- Filtering or searching stories within SubjectView
- Inline editing of story metadata from SubjectView
- Reordering stories through drag-and-drop or controls
- Full StoryView rendering nested within SubjectView
- Custom templates for individual story cards
- Story card customization beyond title and link
- Pagination for large story lists
- Story grouping or categorization
- Story statistics or metadata aggregation
- Interactive story card actions (edit, delete, duplicate)
