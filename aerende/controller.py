# -*- coding: utf-8 -*-

"""
aerende.controller
------------------

This module contains the KeyHandler to handle kepresses, as well as the note
editing and UI manipulating Controller.
"""

from pathlib import Path
import yaml
from os import path
from urwid import MainLoop, ExitMainLoop
from functools import reduce
from collections import Counter

from .models import Note, Tag


class KeyHandler(object):
    """ Handles key input. Behaviour depends on whether aerende is in editor
    mode or not. In editor mode, the keys are just passed to the focused
    editor. Otherwise, the keyhandler checks whether the supplied key is in the
    key -> function map and, if so, executes the mapped function.
    """

    KEY_TO_FUNC_MAP = {

        # Note Creation, Deletion and Editing

        'new_note': lambda self: self.controller.show_note_editor(
            self.controller.edit_note_handler),
        'delete_note': lambda self: self.controller.delete_focused_note(),
        'edit_note': lambda self: self.controller.show_note_editor(
            self.controller.edit_note_handler, True),
        'increment_note_priority': lambda self:
            self.controller.change_focused_note_priority(1),
        'super_increment_note_priority': lambda self:
            self.controller.change_focused_note_priority(10),
        'decrement_note_priority': lambda self:
            self.controller.change_focused_note_priority(-1),
        'super_decrement_note_priority': lambda self:
            self.controller.change_focused_note_priority(-10),

        # Note Navigation

        'next_note': lambda self: self.controller.focus_next_note(),
        'previous_note': lambda self: self.controller.focus_previous_note(),

        # Misc Aerende

        'quit': lambda self: self.controller.exit(),
    }

    def __init__(self, controller, config):
        self.controller = controller
        self.config = config
        self.editor = False

    def handle(self, input, *args, **kwargs):
        if self.is_keyboard_input(input):
            key = ''.join(input)
            self.handle_key(key)

    def keybound_function(self, key):
        """ Given a key, checks whether the key has been defined in the config
        and what key identifier this maps to. Then, returns the controller
        function from the KEY_TO_FUNC_MAP.
        """

        for function, bound_keys in self.config.get_key_bindings().items():
            if key in bound_keys:
                return self.KEY_TO_FUNC_MAP[function]

        return None

    def is_keyboard_input(self, input):
        if input:
            return reduce(lambda x, y: x and y,
                          map(lambda s: isinstance(s, str), input))

    def handle_key(self, key):
        """ Handles a given key. If the controller is in editor mode, the key
        is passed to the current editor. Otherwise, it checks what function
        (if any) the key is bound to, and executes the mapped function.
        """

        if self.controller.editor_mode:
            size = 20
            self.editor.keypress(size, key)
            return

        if not self.controller.editor_mode:
            keybound_function = self.keybound_function(key)
            if keybound_function:
                keybound_function(self)


class Controller(object):
    """ The controller for aerende.
    Reacts to keypresses via the key handler. Is responsible for reading and
    writing notes to the filesystem, and manipulating the underlying urwid
    interface.

    Also responsible for exiting aerende.
    """

    def __init__(self, config, interface):
        self.config = config
        self.data_path = path.expanduser(self.config.get_data_path())
        self.notes = self.load_notes(self.data_path)
        self.tags = self.load_tags(self.notes)
        self.interface = interface
        self.editor_mode = False

        self.key_handler = KeyHandler(self, config)
        self.loop = MainLoop(interface,
                             config.get_palette(),
                             input_filter=self.key_handler.handle)
        self.refresh_interface()
        self.interface.focus_first_note()
        self.loop.run()

    # [ Filesystem Reading / Writing ]

    def load_notes(self, path):
        """ Loads notes from a given file path.
        If no notes file exists at this location, creates an empty one.
        """

        if Path(path).is_file():
            with open(path, 'r') as data_file:
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
            open(path, 'x')
            return []

    def write_notes(self, path):
        """ Writes the current note list to the given file path.
        """

        with open(path, 'w') as data_file:
            for note in self.notes:
                yaml.dump(note.to_dictionary(),
                          data_file,
                          default_flow_style=False)

    # [ Note Creation, Updating and Deletion ]

    def create_note(self, title, tags, text):
        """ Creates a new note object, given the title/tags/text, and appends
        it to the current note list.
        """

        note = Note(title, tags, text)
        self.notes.append(note)

    def delete_note(self, unique_id):
        """ Deletes a note from the current note list, given a note UUID.
        """

        for index, note in enumerate(self.notes):
            if note.id == unique_id:
                del self.notes[index]
                break

    def update_note(self, new_note):
        """ Update a note in the current note list to a given new note.
        """

        for index, note in enumerate(self.notes):
            if note.id == new_note.id:
                note = new_note
                break

    def delete_focused_note(self):
        """ Deletes the focused note. Gets the currently focused note object,
        deletes it from the current note list and writes the note list to file.
        """

        note = self.interface.get_focused_note()
        self.delete_note(note.id)
        self.write_notes(self.data_path)

        self.refresh_interface()

    def change_focused_note_priority(self, amount):
        """ Changes the focused note priority by a given amount. First, gets
        the focused note and changes the priority of the note. Then writes the
        note list to file.
        """

        note = self.interface.get_focused_note()
        note.change_priority(amount)
        self.write_notes(self.data_path)
        self.refresh_interface()

    # [ Tag Loading ]

    def load_tags(self, notes):
        """ Returns a list of tag widgets from a list of notes. Does this by
        first getting all the tags from all the notes in the list. It then
        counts the frequency of these notes, then creates the requisite tag
        widgets from this tag: frequency list.
        """

        note_tags = list(map((lambda note: note.tags), notes))
        note_tags = [tag for subtags in note_tags for tag in subtags]
        tag_frequency = Counter(note_tags)

        tag_widgets = list(
            map((lambda tag: Tag(tag, tag_frequency[tag])), tag_frequency))
        tag_widgets.insert(0, Tag('ALL', len(note_tags)))
        return tag_widgets

    # [ Interface Manipulation ]

    def refresh_interface(self):
        """ Refreshes the interface with the current note and tag lists.
        """

        self.interface.draw_notes(self.notes)
        self.tags = self.load_tags(self.notes)
        self.interface.draw_tags(self.tags)

    def show_note_editor(self, note_handler, edit_focused_note=False):
        """ Shows the note editor at the bottom of the interface.
        If the editor is to edit the focused note, rather than a new one,
        then the focused note is retrieved and passed to the interface.
        """

        note_to_edit = None
        if edit_focused_note:
            note_to_edit = self.interface.get_focused_note()
        self.editor_mode = True
        self.interface.show_note_editor(note_handler, note_to_edit)
        self.key_handler.editor = self.interface.get_note_editor()

    def edit_note_handler(self, note, original_note=None):
        """ Handles the return signal from the note editor. If the note is
        not None (which happens if the user presses escape, cancelling the
        editor), then either a new note is created or an existing note is
        updated, depending on whether the original note returned exists.
        """

        if note is not None:
            title = note[0]
            tags = self._convert_tag_input(note[1])
            text = note[2]
            if original_note is not None:
                original_note.edit_note(title, tags, text)
                self.update_note(original_note)
            else:
                self.create_note(title, tags, text)
            self.write_notes(self.data_path)

            # Restart the loop.. Seems to work?
            self.loop.stop()
            self.loop.start()

        self.refresh_interface()
        self.editor_mode = False

    def _convert_tag_input(self, tag_text):
        split_tags = tag_text.split('//')
        return list(map(lambda tag: tag.strip(), split_tags))

    def focus_next_note(self):
        self.interface.focus_next_note()

    def focus_previous_note(self):
        self.interface.focus_previous_note()

    # [ System Functions ]

    def exit(self):
        raise ExitMainLoop()
