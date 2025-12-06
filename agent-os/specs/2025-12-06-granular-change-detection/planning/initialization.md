# Spec Initialization: Granular Change Detection

## User Description
"17 granular change detection"

## Context from Roadmap

From the product roadmap (feature #17):

> Granular change detection — Make the change detection more granular. First, track the currently-viewed page. If it is not a Story, then keep as-is. If a Story, keep track of which Story and only do reloading if the change is about the currently-viewed story. If the `themed_story.html` or any of its assets are in the changeset, tell the iframe to reload. If it is the Story index.html, don't do a reload. Instead, send the HTML in the payload and use a local copy of https://github.com/bigskysoftware/idiomorph to patch the page. Explain this in the architecture documents.

**Size Estimate:** M (Medium)

**Status:** Not started ([] in roadmap)

## Related Features

This feature builds on:
- Feature #4: Hot Reload Development Server (completed) - provides the foundation of file watching and browser refresh
- Feature #8: Themed Stories (completed) - the themed stories shown in iframes are part of what needs granular reloading
- Feature #10: Update Docs (completed) - architecture documentation needs updates for this feature

## Product Context

Storyville is a Python-native component development platform that provides a Storybook-like experience. The hot reload system currently refreshes the entire page when any file changes, but this feature aims to make reloading more intelligent and performant by:
- Only reloading content relevant to the currently-viewed page
- Using iframe reloads for themed story content
- Using DOM morphing (idiomorph) for non-iframe content to avoid full page refreshes
