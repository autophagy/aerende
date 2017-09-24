from pathlib import Path
import yaml
from os import path
import uuid
from urwid import MainLoop

from .configuration import PALETTE
from .models import Note


class Controller(object):

    def __init__(self, config, interface):
        self.config = config
        self.data_path = path.expanduser(self.config['data_path'])
        self.notes = self.load_notes()

        loop = MainLoop(interface, PALETTE)
        interface.draw_notes(self.notes)
        loop.run()

    def load_notes(self):
        # If no notes, create empty file
        if Path(self.data_path).is_file():
            with open(self.data_path, 'r') as data_file:
                note_yaml = yaml.load(data_file)
                notes = []

                if note_yaml is None:
                    return notes

                for note_yaml_item in note_yaml:
                    for unique_id, note in note_yaml_item.items():
                        notes.append(Note(note['title'],
                                          note['tags'],
                                          note['text'],
                                          note['priority'],
                                          unique_id))
                return notes
        else:
            open(self.data_path, 'x')
            return []

    def write_notes(self):
        with open(self.data_path, 'w') as data_file:
            yaml.dump(self.notes, data_file, default_flow_style=False)

    def create_note(self, title, tags, text):
        note = Note(title, tags, text)
        self.notes.append(note.to_dictionary())

    def delete_note(self, unique_id):
        del self.notes[unique_id]

    def exit(self):
        exit()
