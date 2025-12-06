# Breadcrumbs Feature Spec

## Initial Idea

From roadmap item #11:

Put the path to the current node in a breadcrumbs-style navigation, in `<main>` above the title. Provide links for each hop. Remove the `Parent` link in the template.

## Context

The breadcrumbs component has been created at `src/storyville/components/breadcrumbs/breadcrumbs.py` and integrated into `LayoutMain`. The component shows a hierarchy like: Home → Section → Subject → Story.

However, based on the code review:

1. The Breadcrumbs component is already integrated into LayoutMain
2. Each view (SectionView, SubjectView, StoryView) still contains `<a href="..">Parent</a>` links that should be removed
3. The current_path parameter needs to be properly passed through all views to the Layout component

## Current State

- Breadcrumbs component: ✅ Implemented
- Integration in LayoutMain: ✅ Done
- Parent links in views: ❌ Still present (needs removal)
- current_path plumbing: ❓ Needs verification
