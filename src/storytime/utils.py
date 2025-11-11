"""Utility functions for Storytime."""

from inspect import getmembers, isfunction
from types import ModuleType
from typing import TYPE_CHECKING, get_type_hints

if TYPE_CHECKING:
    from storytime.section import Section
    from storytime.site import Site
    from storytime.subject import Subject


def get_certain_callable(module: ModuleType) -> "Site | Section | Subject | None":
    """Return the first Site/Section/Subject in given module that returns correct type.

    A ``stories.py`` file should have a function that, when called,
    constructs an instance of a Section, Subject, etc. This helper
    function does the locating and construction. If no function
    is found with the correct return value, return None.

    We do it this way instead of magically-named functions, meaning,
    we don't do convention over configuration.

    Args:
        module: A stories.py module that should have the right function.

    Returns:
        The Site/Section/Story instance or ``None`` if there wasn't an
        appropriate function.
    """
    from storytime.section import Section
    from storytime.site import Site
    from storytime.subject import Subject

    valid_returns = (Site, Section, Subject)
    for _name, obj in getmembers(module):
        if isfunction(obj) and obj.__module__ is module.__name__:
            th = get_type_hints(obj)
            return_type = th.get("return")
            if return_type and return_type in valid_returns:
                # Call the obj to let it construct and return the
                # Site/Section/Subject
                target: Site | Section | Subject = obj()
                return target

    # We didn't find an appropriate callable
    return None
