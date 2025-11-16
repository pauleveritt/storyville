# Spec Requirements: Better Examples

## Initial Description

Better examples. Let's update the `examples` directory to have a rich set of usages that match all the features and
functionality in Section/Subject/Story. Find all combinations of ways that a Story can be used and write components that
can exercise those Story features. Have some with title or description, some without. In each example, write a README
explaining what that example is showing. Then, update `test_examples` to exercise each example. Each example test should
render each part of the Site tree (each Section/Subject/Story) and use aria-testing to ensure we get what we expect from
the components etc. being rendered.

**Context:**
This is for the Storytime project - a Python library for organizing component stories/documentation similar to
Storybook.

Key models in the codebase:

- Site: Top-level container for stories
- Section: Organizational grouping within a Site
- Subject: Represents a component being documented
- Story: Individual story/example of a component

Current examples directory has minimal examples. We need comprehensive examples showing all feature combinations.

## Requirements Discussion

### First Round Questions

**Q1:** I assume we should create examples demonstrating all optional field combinations for each model (Site, Section,
Subject, Story). This would include combinations of title/description presence/absence, custom templates, prop
variations, and target specifications. Is that correct?

**Answer:** YES - Create examples demonstrating all optional field combinations for each model.

**Q2:** I'm thinking we should demonstrate all variations of Story usage, including:

- Story with props only (inheriting target from Subject)
- Story with its own target (overriding Subject's target)
- Story with custom template
- Story with title and description
- Story with minimal configuration
- Stories with different prop combinations for the same component

Should we cover all these variations?

**Answer:** YES - Demonstrate all variations:

- Story with props only (inheriting target from Subject)
- Story with its own target (overriding Subject's target)
- Story with custom template
- Story with title and description
- Story with minimal configuration
- Stories with different prop combinations for the same component

**Q3:** For example structure, I assume each example subdirectory should contain:

- A `stories.py` file defining the Site
- Nested directories for Sections (each with `stories.py`)
- Nested component directories for Subjects (each with `stories.py`)
- A README.md explaining what feature combinations that example demonstrates

Is this the structure you want?

**Answer:** YES - Each example subdirectory should contain:

- A `stories.py` file defining the Site
- Nested directories for Sections (each with `stories.py`)
- Nested component directories for Subjects (each with `stories.py`)
- A README.md explaining what feature combinations that example demonstrates

**Q4:** For test coverage, each test should:

- Load a Site using `make_site()` from the example package
- Traverse the tree (Site → Sections → Subjects → Stories)
- Render each Story's component
- Use aria-testing to verify expected ARIA attributes/roles
- Validate the hierarchical structure is correct
- Verify title/description fields are properly inherited or set

Does this match your expectations for test_examples?

**Answer:** YES, with addition - Each test should:

- Load a Site using `make_site()` from the example package
- Traverse the tree (Site → Sections → Subjects → Stories)
- Render each Story's component
- Use aria-testing to verify expected ARIA attributes/roles
- Validate the hierarchical structure is correct
- Verify title/description fields are properly inherited or set
- **ADDITIONAL:** Render each part of the tree with its view and use aria-testing to confirm. Section uses SectionView,
  Subject uses SubjectView, Story uses StoryView.

**Q5:** Should we include components with varying complexity levels (simple buttons, complex forms, components with
multiple props, nested children, various accessibility patterns, form components, layout components) to thoroughly test
the Story system?

**Answer:** NO - Keep the components simple for now. Don't include complex components with multiple props, nested
children, various accessibility patterns, or form/layout components.

**Q6:** For ARIA testing, should we verify:

- Standard ARIA attributes (roles, labels, states)
- Specific semantic HTML elements expected
- ARIA relationships (describedby, labelledby, etc.)
- Interactive component states (expanded, selected, etc.)

Or should we focus on a subset?

**Answer:** NO - Focus on standard ARIA attributes (roles, labels, states) only. Don't test for specific semantic HTML
elements, ARIA relationships, or interactive component states.

**Q7:** I'm thinking we should organize examples into these categories:

- `minimal` (already exists - keep/update as needed)
- `complete` (showing all features)
- `inheritance` (demonstrating how props/titles inherit)
- `templates` (showing custom template usage)
- `no_sections` (already exists - direct Subject under Site)

Should we use these example directories?

**Answer:** YES - Create these example directories:

- `minimal` (already exists - keep/update as needed)
- `complete` (showing all features)
- `inheritance` (demonstrating how props/titles inherit)
- `templates` (showing custom template usage)
- `no_sections` (already exists - direct Subject under Site)

**Q8:** What should we explicitly NOT include in this work? For example:

- Performance testing of large Sites with hundreds of stories
- Testing the web browser UI itself
- Integration with external frameworks (Django, Flask, FastAPI)
- Hot reload functionality

**Answer:** YES - Explicitly exclude:

- Performance testing of large Sites
- Testing the web browser UI itself
- Integration with external frameworks (Django/Flask/FastAPI)
- Hot reload functionality

### Existing Code to Reference

**Q9:** Are there existing features in your codebase with similar patterns we should reference? For example:

- Similar interface elements or UI components to re-use
- Comparable page layouts or navigation patterns
- Related backend logic or service objects
- Existing models or controllers with similar functionality

Please provide file/folder paths or names of these features if they exist.

**Answer:** NO - No existing features with similar patterns to reference. Create from scratch.

### Visual Assets

**Q10:** Do you have any design mockups, wireframes, or screenshots that could help guide the development?

**Answer:** NO - No design mockups, wireframes, or screenshots provided.

**Visual Check Result:** No visual files found in planning/visuals/ directory.

## Visual Assets

### Files Provided:

No visual assets provided.

## Requirements Summary

### Functional Requirements

**Core Functionality:**

- Update the `examples/` directory with comprehensive examples demonstrating all feature combinations
- Create examples for all optional field combinations across Site, Section, Subject, and Story models
- Include Story variations: props-only, custom target, custom template, title/description, minimal config, and prop
  combinations
- Each example must have a README.md explaining the feature combinations it demonstrates
- Update `test_examples` to exercise each example comprehensively

**Example Structure:**

- Each example subdirectory contains:
    - `stories.py` file defining the Site
    - Nested directories for Sections (each with `stories.py`)
    - Nested component directories for Subjects (each with `stories.py`)
    - README.md explaining feature combinations demonstrated

**Example Categories (Directories):**

1. `minimal` - Already exists, keep/update as needed
2. `complete` - Showing all features
3. `inheritance` - Demonstrating how props/titles inherit
4. `templates` - Showing custom template usage
5. `no_sections` - Already exists, direct Subject under Site

**Story Variations to Demonstrate:**

- Story with props only (inheriting target from Subject)
- Story with its own target (overriding Subject's target)
- Story with custom template
- Story with title and description
- Story with minimal configuration
- Stories with different prop combinations for the same component

**Test Coverage:**
Each test must:

- Load a Site using `make_site()` from the example package
- Traverse the tree (Site → Sections → Subjects → Stories)
- Render each Story's component using aria-testing
- Render each part of the tree with its corresponding view:
    - Section uses SectionView
    - Subject uses SubjectView
    - Story uses StoryView
- Use aria-testing to verify expected ARIA attributes/roles for each rendered view
- Validate the hierarchical structure is correct
- Verify title/description fields are properly inherited or set

**Component Complexity:**

- Keep components simple
- Do NOT include:
    - Complex components with multiple props
    - Nested children
    - Various accessibility patterns
    - Form components
    - Layout components

**ARIA Testing Focus:**

- Standard ARIA attributes only (roles, labels, states)
- Do NOT test for:
    - Specific semantic HTML elements
    - ARIA relationships (describedby, labelledby, etc.)
    - Interactive component states (expanded, selected, etc.)

### Reusability Opportunities

No similar existing features identified for reference. This work will be created from scratch.

### Scope Boundaries

**In Scope:**

- Updating/creating examples in the `examples/` directory
- Creating comprehensive Story variations demonstrating all optional field combinations
- Writing README.md files for each example explaining feature combinations
- Updating `test_examples` to:
    - Load Sites from example packages
    - Traverse Site → Section → Subject → Story hierarchies
    - Render components and views with aria-testing
    - Validate structure and field inheritance
- Simple component examples
- Testing standard ARIA attributes (roles, labels, states)
- Five example categories: minimal, complete, inheritance, templates, no_sections

**Out of Scope:**

- Performance testing of large Sites with many stories
- Testing the web browser UI itself
- Integration with external frameworks (Django, Flask, FastAPI)
- Hot reload functionality
- Complex components with multiple props, nested children, or advanced accessibility patterns
- Form or layout components
- Testing specific semantic HTML elements
- Testing ARIA relationships (describedby, labelledby, etc.)
- Testing interactive component states (expanded, selected, etc.)

### Technical Considerations

**Testing Framework:**

- Use aria-testing library for ARIA attribute verification
- Tests must render both components and views (SectionView, SubjectView, StoryView)
- Each example should have its own test module in `test_examples`

**Project Structure:**

- Maintain existing `examples/` directory structure
- Keep existing `minimal` and `no_sections` examples (update as needed)
- Add new examples: `complete`, `inheritance`, `templates`
- Each example is a Python package with `make_site()` function

**Quality Standards:**

- All tests must pass: `just test`
- Type checking must pass: `just typecheck`
- Code must be formatted: `just fmt`
- Follow modern Python 3.14+ standards including structural pattern matching, type statement, and PEP 604 union syntax

**Model Fields to Exercise:**
Based on Storytime models, examples should demonstrate optional field combinations for:

- Site: title, description, template variations
- Section: title, description, template variations
- Subject: title, description, target, template variations
- Story: title, description, target (override), props, template variations
