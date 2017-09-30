from pathlib import Path
import yaml
from os import path
import uuid
from urwid import MainLoop

from .configuration import PALETTE
from .models import Note, Tag


class Controller(object):

    def __init__(self, config, interface):
        self.config = config
        self.data_path = path.expanduser(self.config['data_path'])
        self.notes = self.load_notes()
        self.tags = self.load_tags(self.notes)
        self.interface = interface

        loop = MainLoop(interface, PALETTE)
        self.refresh_interface()
        loop.run()

    def load_notes(self):
        # If no notes, create empty file
        if Path(self.data_path).is_file():
            with open(self.data_path, 'r') as data_file:
                note_yaml = yaml.load(data_file)
                notes = []

                if note_yaml is None:
                    return notes

                for unique_id, note in note_yaml.items():
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
            for note in self.notes:
                yaml.dump(note.to_dictionary(), data_file, default_flow_style=False)

    def create_note(self, title, tags, text):
        note = Note(title, tags, text)
        self.notes.append(note)

    def delete_note(self, unique_id):
        del self.notes[unique_id]

    def load_tags(self, notes):
        tags = {'ALL': 0}
        tag_widgets = []
        for note in notes:
            tags['ALL'] += 1
            for tag in note.tags:
                if tag in tags:
                    tags[tag] += 1
                else:
                    tags[tag] = 1
        for tag in tags:
            tag_widgets.append(Tag(tag, tags[tag]))
        return tag_widgets

    def refresh_interface(self):
        self.interface.draw_notes(self.notes)
        self.tags = self.load_tags(self.notes)
        self.interface.draw_tags(self.tags)

    def exit(self):
        exit()
