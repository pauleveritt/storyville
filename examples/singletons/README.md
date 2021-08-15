# Singletons

If you're using a registry for your components, Storytime makes it easy to put some singletons into the registry being created.

You can pass in a list of instances to register.
If you want a singleton registered as a different "kind", pass in a tuple with the instance and the kind.

In the `Heading` example, singletons are provided from "up above". 
In this case, the `Subject`.
In the `Another Heading` example, singletons are stamped on the individual story.