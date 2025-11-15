# Feature Idea: Render a Single Story

Render a single Story. A Story should have a StoryView which receives the `story: Story` and uses a tdom template and
possibly some components to return a tdom.Element. You might need to do some type guard to convert tdom.Node to
tdom.Element before returning.
