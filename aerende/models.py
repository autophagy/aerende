import uuid


class Note(object):
    """
    A note.
    Currently has a title, tags, texr and a priority."""

    def __init__(self, title, tags, text, priority=1, unique_id=None):
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
        return list(set(tags))

    def to_dictionary(self):
        return {
            self.id: {
                'title': self.title,
                'tags': self.tags,
                'text': self.text,
                'priority': self.priority,
            }
        }

    def increment_priority(self):
        self.priority += 1

    def decrement_priority(self):
        self.priority = 0 if self.priority - 1 < 0 else self.priority - 1

    def formatted_tags(self):
        return " // ".join(self.tags)

    def edit_note(self, title, tags, text):
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
