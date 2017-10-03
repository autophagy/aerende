from pathlib import Path
import yaml
from os import path
import uuid
from urwid import MainLoop, ExitMainLoop
from functools import reduce

from .configuration import PALETTE, KEY_BINDINGS
from .models import Note, Tag


class KeyHandler(object):

    def __init__(self, controller):
        self.controller = controller
        self.editor = False

    def handle(self, input, *args, **kwargs):
        if self.is_keyboard_input(input):
            key = ''.join(input)
            self.handle_key(key)

    def is_key_bound(self, key, name):
        try:
            bound_key = KEY_BINDINGS[name]
        except KeyError:
            return False
        else:
            return key == bound_key

    def is_keyboard_input(self, input):
        if input:
            return reduce(lambda x, y: x and y,
                          map(lambda s: isinstance(s, str), input))

    def handle_key(self, key):
        if self.controller.editor_mode:
            size = 20
            self.editor.keypress(size, key)
            return

        if not self.controller.editor_mode:
            if self.is_key_bound(key, 'new_note'):
                self.controller.show_note_editor()
            elif self.is_key_bound(key, 'quit'):
                self.controller.exit()


class Controller(object):

    def __init__(self, config, interface):
        self.config = config
        self.data_path = path.expanduser(self.config['data_path'])
        self.notes = self.load_notes()
        self.tags = self.load_tags(self.notes)
        self.interface = interface
        self.editor_mode = False

        self.key_handler = KeyHandler(self)
        self.loop = MainLoop(interface,
                             PALETTE,
                             input_filter=self.key_handler.handle)
        self.refresh_interface()
        self.loop.run()

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
                yaml.dump(note.to_dictionary(),
                          data_file,
                          default_flow_style=False)

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

    def show_note_editor(self):
        self.editor_mode = True
        self.interface.show_note_editor(self.edit_note_handler)
        self.key_handler.editor = self.interface.get_note_editor()

    def edit_note_handler(self, note):
        if note is not None:
            title = note[0]
            tags = self._convert_tag_input(note[1])
            text = note[2]

            self.create_note(title, tags, text)
            self.write_notes()

            # Restart the loop.. Seems to work?
            self.loop.stop()
            self.loop.start()

        self.refresh_interface()
        self.editor_mode = False

    def _convert_tag_input(self, tag_text):
        split_tags = tag_text.split('//')
        return list(map(lambda tag: tag.strip(), split_tags))

    def exit(self):
        raise ExitMainLoop()
