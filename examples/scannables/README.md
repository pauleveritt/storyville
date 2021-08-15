# Scannables

If you're using a registry for your components, Storytime makes it easy to grab some injectables.
Starting at the `Site`, any node in the tree can pass in a `scannables` value to the constructor.
This is a full dotted-path-package-name pointing at something to import and scan (using `Venusian`) for registrations.

Usually you just say "YOLO" and register everything in your package by putting a `scannables` (or `plugins`) on your `Site`.
But you might prefer some isolation in your tree, with each node making a subregistry that has only the registrations needed in that part.
This makes dependencies more explicit.
