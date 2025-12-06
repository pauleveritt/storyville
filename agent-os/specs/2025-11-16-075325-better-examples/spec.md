# Specification: Better Examples for Storyville

## Goal

Create comprehensive examples demonstrating all feature combinations across Site, Section, Subject, and Story models
with complete test coverage using aria-testing to verify both component rendering and view hierarchies.

## User Stories

- As a Storyville evaluator, I want to see an example of the system and why I should be interested
- As a Storyville user, I want to see examples of all Story variation patterns so that I understand how to use optional
  fields and inheritance
- As a developer, I want comprehensive test coverage for all examples so that I can verify the Storyville library works
  correctly across different configurations

## Specific Requirements

**Example Directory Structure**

- Each example is a Python package under `examples/` with `stories.py` at root
- Some examples have no `__init__.py` in the hierarchy, some of a few places with `__init__.py`, some have all
  directories with `__init__.py`
- Nested directories for Sections contain their own `stories.py` files
- Component directories under Sections contain `stories.py` files defining Subjects
- Each example root contains a `README.md` explaining the feature combinations demonstrated
- Use `make_site(package_location)` to load and build the complete Site tree from any example package

**Minimal Example Updates**

- Keep existing `examples/minimal/` structure as-is
- Add `README.md` documenting that this shows the most basic usage: one Section, one Subject, one Story with props only
- Update `examples/minimal/stories.py` to use `this_site()` function (currently uses wrong function name)
- Keep the single Heading component with single Story using props inheritance from Subject target

**Complete Example**

- Create `examples/complete/` demonstrating all optional fields across all models
- Site with title and description defined
- One Section with title and description
- One Subject with title, description, and target component
- Three Stories demonstrating: (1) minimal props-only, (2) Story with custom title and description, (3) Story with
  different prop combinations for same component
- Simple component (e.g., Button accepting text and variant props)
- README explaining this shows all optional Site/Section/Subject/Story fields populated

**Inheritance Example**

- Create `examples/inheritance/` demonstrating field inheritance patterns
- Show how Story inherits target from Subject when not specified
- Show how Story title is auto-generated from Subject title when not specified
- One Subject with target defined, multiple Stories: some with explicit titles, some inheriting auto-generated titles
- One Story demonstrating target override (Story specifies its own target different from Subject)
- README explaining inheritance rules: target inheritance, title generation, and parent relationships

**Templates Example**

- Create `examples/templates/` demonstrating custom template usage
- One Subject with standard target component
- Two Stories: (1) Story without template (uses default StoryView layout), (2) Story with custom template function
  overriding all rendering
- Custom template demonstrates full control over rendering using tdom html t-string
- README explaining template override behavior and when to use custom templates

**No Sections Example Updates**

- Keep existing `examples/no_sections/` structure showing direct Subject under Site without Section
- Add `README.md` documenting this demonstrates the optional nature of Sections in the hierarchy
- Verify the example has Subject directly under Site in tree structure

**Simple Component Patterns**

- All example components use simple tdom-based callable components returning Node
- Components use dataclass pattern with `__call__` method returning `html(t"...")` result
- Maximum 2-3 props per component (e.g., name, text, variant, count)
- No complex nested children, forms, layouts, or advanced accessibility patterns

**Test Structure for Each Example**

- Create `tests/test_examples.py` with one test function per example
- Each test loads Site using `make_site("examples.[example_name]")`
- Each test traverses the full tree: Site items to Sections, Section items to Subjects, Subject items to Stories
- Use structural pattern matching (`match`/`case`) to verify node types during traversal
- Validate hierarchical structure is correct (parent references, name fields, package_path values)

**Component Rendering Tests**

- For each Story in each example, render `story.instance` to get the component output
- Use aria-testing functions (`get_by_tag_name`, `get_text_content`, `query_all_by_tag_name`) to verify component
  rendering
- Verify standard ARIA attributes: roles, labels, states only
- Do not test semantic HTML elements, ARIA relationships, or interactive states
- Focus on verifying the component rendered with expected prop values

**View Rendering Tests**

- For each Section, create `SectionView(section=section)` and call it to render
- For each Subject, create `SubjectView(subject=subject)` and call it to render
- For each Story, create `StoryView(story=story)` and call it to render
- Use aria-testing to verify view-specific elements (h1 titles, description paragraphs, navigation links)
- Verify all view results are Element instances (type guard with `isinstance(result, Element)`)
- Check that titles, descriptions, and props display correctly in each view

**Field Inheritance Validation**

- Verify Story inherits target from Subject when `story.target is None`
- Verify Story generates title from Subject when `story.title is None`
- Check that explicitly set Story titles and targets override inheritance
- Validate parent references are correctly assigned throughout tree

**README Documentation Requirements**

- Each README uses markdown with heading structure
- Include "Overview" section explaining what features the example demonstrates
- Include "Structure" section describing the file/directory organization
- Include "Key Features" section with bullet points of specific patterns shown
- Keep READMEs concise (under 20 lines) focused on example-specific information

## Visual Design

No visual assets provided.

## Existing Code to Leverage

**make_site() function from storyville.site.helpers**

- Use `make_site(package_location: str) -> Site` to load any example package
- Automatically discovers all `stories.py` files via rglob and builds complete tree
- Handles Site/Section/Subject instantiation and parent/child relationships
- Returns fully constructed Site with populated items dictionaries

**View classes for rendering**

- `SectionView(section=section)` renders Section with title, description, subject cards, parent link
- `SubjectView(subject=subject)` renders Subject with title, target info, story cards, parent link
- `StoryView(story=story)` renders Story with dual modes: custom template or default layout
- All views implement `__call__() -> Node` protocol and return tdom Element instances

**aria-testing patterns from existing tests**

- Use `get_by_tag_name(element, "h1")` to find specific element types
- Use `get_text_content(element)` to extract text from rendered elements
- Use `query_all_by_tag_name(element, "p")` to find multiple elements
- Use `isinstance(result, Element)` type guard to verify view return types
- Check element attributes with `element.attrs.get("href")` pattern

**Simple component pattern from Heading**

- Dataclass-based component with props as fields
- Implement `__call__(self) -> Node` method
- Return `html(t"<tag>{self.prop}</tag>")` using tdom t-strings
- Components are callables that construct Node instances when invoked

**TreeNode and tree traversal from storyville.nodes**

- `TreeNode` handles package location resolution and story module imports
- `get_certain_callable(module)` finds and calls the Site/Section/Subject factory function
- Tree nodes track parent paths, package locations, and names
- Use `site.items` dict for Sections, `section.items` dict for Subjects, `subject.items` list for Stories

## Out of Scope

- Performance testing of large Sites with hundreds or thousands of stories
- Testing the web browser UI, JavaScript interactions, or visual rendering
- Integration with external frameworks like Django, Flask, or FastAPI
- Hot reload functionality or file watching during development
- Complex components with multiple nested children or advanced props
- Form components with validation, submission, or input handling
- Layout components or grid systems
- Testing specific semantic HTML elements beyond basic tag verification
- Testing ARIA relationships like describedby, labelledby, or owns
- Testing interactive component states like expanded, selected, pressed, or checked
- Custom view templates for Site, Section, or Subject (only Story templates)
