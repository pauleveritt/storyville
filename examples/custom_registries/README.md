# Custom Registries

By default, the `Site` at the root, behind the scenes, makes a registry.
This registry is then setup and passed down to `Section`, `Subject`, and `Story`.

A `Site` though can pass-in its own registry, constructed its own way.
That custom registry will then be used instead of an implicitly-constructed registry.
Also, a `Section` or `Subject` or `Story` can pass in a registry during construction.
This registry intercepts the handed-down registry, meaning `self.registry.parent` is `None`.

Whenever a node in the tree passed in a registry, it divorces that level and children from any registrations done earlier.
It provides isolation.

As one last note, all of these -- `Site`, `Section`, `Subject`, `Story` -- can be passed in some registry _modifiers._
These include `plugins`, `scannables`, etc.
In _this_ case, the handed-down registry is kept as a parent registry.
When this is done, here's what happens with the registry for that level in the tree and below:

- If a registry was also passed in, use it
- If _no_ registry was passed in...we need to make a new one to isolate _new_ registrations to just that part of the tree
- The new registry assigns the handed-down one as the `.parent` registry
- The new registry, with the new registrations and context, gets passed down to the stuff below
