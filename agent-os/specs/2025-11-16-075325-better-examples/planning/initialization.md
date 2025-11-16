# Spec Initialization: Better Examples

**Feature Description:**
Better examples. Let's update the `examples` directory to have a rich set of usages that match all the features and functionality in Section/Subject/Story. Find all combinations of ways that a Story can be used and write components that can exercise those Story features. Have some with title or description, some without. In each example, write a README explaining what that example is showing. Then, update `test_examples` to exercise each example. Each example test should render each part of the Site tree (each Section/Subject/Story) and use aria-testing to ensure we get what we expect from the components etc. being rendered.

**Context:**
This is for the Storytime project - a Python library for organizing component stories/documentation similar to Storybook.

Key models in the codebase:
- Site: Top-level container for stories
- Section: Organizational grouping within a Site
- Subject: Represents a component being documented
- Story: Individual story/example of a component

Current examples directory has minimal examples. We need comprehensive examples showing all feature combinations.

**Timestamp:** 2025-11-16-075325
