# Templates Example

## Overview

Demonstrates custom template usage for Stories, showing how templates can completely override the default StoryView rendering.

## Structure

- Site: Templates Example
- Section: Template Components
- Subject: Alert component
- Story 1: Uses default StoryView layout (template=None)
- Story 2: Uses custom template function (template=custom_alert_template)

## Key Features

- **Default StoryView Layout**: When story.template is None, renders standard layout with title, props, component, and parent link
- **Custom Template Override**: When story.template is set, the template function has complete control over rendering using tdom t-string
- **Use Cases**: Custom templates are useful when you need full control over story presentation, bypassing the default layout entirely
