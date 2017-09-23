import uuid

class Note(object):
    """
    A note.
    Currently has a title, tags, texr and a priority."""
    def __init__(self, title, tags, text, priority = 1, unique_id = None):
        if unique_id is None:
            self.id = str(uuid.uuid4())
        else:
            self.id = unique_id
        self.title = title
        self.tags = tags
        self.text = text
        self.priority = priority

    def __str__(self):
        return str(self.to_dictionary)

    def to_dictionary(self):
        return {
            self.id: {
                'title': self.title,
                'tags': str(self.tags),
                'text': self.text,
                'priority': self.priority,
            }
        }
