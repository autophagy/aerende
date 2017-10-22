from aerende.models import Note

import unittest


def init_note(**kwargs):
    default_note_args = {
        'title': 'Motoko',
        'tags': ['Batou', 'Togusa'],
        'text': 'Just a whisper. I hear it in my ghost.',
        'priority': 1,
        'unique_id': None
    }
    default_note_args.update(kwargs)
    return Note(**default_note_args)


class TestNoteModel(unittest.TestCase):

    def test_note_initialisation(self):
        title = 'Akira'
        tags = ['Tetsuo', 'Kaneda']
        text = 'What did you people do to my head?'
        priority = 100
        unique_id = '12345'
        note = init_note(title=title,
                         tags=tags,
                         text=text,
                         priority=priority,
                         unique_id=unique_id)

        self.assertEqual(title, note.title)
        self.assertEqual(sorted(tags), sorted(note.tags))
        self.assertEqual(text, note.text)
        self.assertEqual(priority, note.priority)
        self.assertEqual(unique_id, note.id)

    def test_tag_verification(self):
        tags = ['a', 'b', 'c']
        repeated_tags = tags*5
        note = init_note(tags=repeated_tags)
        self.assertEqual(sorted(tags), sorted(note.tags))

    def test_priority(self):
        note = init_note(priority=5)

        note.change_priority(10)
        self.assertEqual(15, note.priority)

        note.change_priority(-5)
        self.assertEqual(10, note.priority)

        # A note's priority cannnot be changed to below zero
        note.change_priority(-100)
        self.assertEqual(0, note.priority)

if __name__ == '__main__':
    unittest.main()
