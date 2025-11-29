# Raw Idea

iframe reloader.

When viewing a Story, I want the updated page to load faster, without disruption of scroll position, and little repaint. I don't want the main HTML in the document to reload. Only the HTML for the iframe.

Instead of triggering a full page reload, the JS event handler should only reload the <iframe> content.
