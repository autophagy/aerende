# -*- coding: utf-8 -*-

"""
aerende.models
-----------

This module contains models for use within aerende. Currently contains 2
models:

Note - A representation of an aerende note, with a title, tag list, text and
       priority.

Tag - A representation of a tag with the number of times that tag occurs.
"""

import uuid


class Note(object):
    """
    A note.
    Currently has a title, tags, text and a priority."""

    def __init__(self, title, tags, text, priority=1, unique_id=None):
        """ If created without a unique_id, it is assumed the note is new
        and so a new uuid is created.
        """
        if unique_id is None:
            self.id = str(uuid.uuid4())
        else:
            self.id = unique_id
        self.title = title
        self.tags = self.__verify_tags(tags)
        self.text = text
        self.priority = priority

    def __str__(self):
        return str(self.to_dictionary)

    def __verify_tags(self, tags):
        """ Removes any duplicate tags from the supplied list.
        """
        return list(set(tags))

    def to_dictionary(self):
        """ Returns a dictionary representation of the object, suitable for
        writing out to YAML.
        """
        return {
            self.id: {
                'title': self.title,
                'tags': self.tags,
                'text': self.text,
                'priority': self.priority,
            }
        }

    def change_priority(self, amount):
        if self.priority + amount < 0:
            self.priority = 0
        else:
            self.priority += amount

    def formatted_tags(self):
        """ Formats the note's tag list for displaying in the UI.
        """
        return " // ".join(self.tags)

    def edit_note(self, title, tags, text):
        """ Updates the note's properties
        """
        self.title = title
        self.tags = tags
        self.tags = self.__verify_tags(tags)
        self.text = text


class Tag(object):
    """A note tag, for categorisation/filtering"""

    def __init__(self, type, frequency):
        self.type = type
        self.frequency = frequency

    def __str__(self):
        return "[{0}] {1}".format(self.frequency, self.type)
