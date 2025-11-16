"""Site for the inheritance example."""


from storytime import Site


def this_site() -> Site:
    """Create the inheritance example site."""
    return Site(title="Inheritance Example")
