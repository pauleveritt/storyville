# Spec Initialization: Layout

## Feature Description

Layout. All the views should use a common component called components/layout. This layout wraps the contents of that view, providing the full `<html>`, `<head>`, and `<body>`. The contents of the view should go in `<main>` in the layout. The view should pass a prop to the layout for what to put in the `<title>`, which will concat with the Site.title such as `<title>{view_title} - {self.title}</title>`.

Layouts will also have an `assets` directory. This asset directory should be copied to the root of the output directory during building, which we will do in the next feature.

## Date Created
2025-11-16

## Status
Initialized - Ready for requirements gathering
