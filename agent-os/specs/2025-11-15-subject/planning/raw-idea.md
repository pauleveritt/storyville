# Raw Idea

A Subject is an entity that collects a group of Story entries about component, a view, or some other visible part of the
system. It should have a parent, a target (the callable component or view etc.) and stories as a list of Story
instances. It should be a Python package with models.py and views.py. We have a start of this in subject.py. Tests
should go in tests/subject/ . The SubjectView will render some markup then the list of Story objects via StoryView. If a
Story does not have a component, and the Subject does, it can pass in the Subject to the StoryView.
