from urwid import (Columns,
                   LineBox,
                   Text,
                   Frame,
                   ListBox,
                   AttrMap,
                   Padding,
                   SimpleListWalker,
                   signals,
                   connect_signal,
                   emit_signal,
                   Edit,
                   WidgetWrap)
from functools import reduce
import sys
import tempfile
import os
from subprocess import call

from . import version, title


class AerendeInterface(Columns):
    """
    Creates the interface for Aerende, as well as providing refresh and drawing
    functions.
    """

    def __init__(self):
        self.notes_frame = NotesFrame([])
        self.tags_list = TagsListBox([])
        Columns.__init__(self, [(18, self.tags_list), self.notes_frame])

    # [ Notes ]

    def draw_notes(self, notes):
        self.contents[1][0].draw_notes(notes)

    # [ Tags ]

    def draw_tags(self, tags):
        tag_list = self.contents[0][0]
        tag_list.draw_tags(tags)
        new_options = self.options('given', tag_list.get_max_width(tags),
                                   False)
        self.contents[0] = (tag_list, new_options)

    def show_note_editor(self, done_handler, note_to_edit=None):
        self.notes_frame.show_note_editor(done_handler, note_to_edit)

    def get_note_editor(self):
        return self.notes_frame.editor

    def focus_next_note(self):
        self.notes_frame.focus_next_note()

    def focus_previous_note(self):
        self.notes_frame.focus_previous_note()

    def focus_first_note(self):
        self.notes_frame.focus_first_note()

    def get_focused_note(self):
        return self.notes_frame.get_focused_note()


class NoteWidget(LineBox):
    """Widget for displaying a note"""

    def __init__(self, note):
        self.note = note

        header = self._create_header(note)
        footer = self._create_footer(note)
        note_display = Text("{0}\n\n{1}\n\n{2}".format(
            header, note.text, footer))
        LineBox.__init__(self, note_display)

    def _create_header(self, note):
        return "{0} :: {1}".format(note.priority, note.title)

    def _create_footer(self, note):
        footer_template = "[ {0} ]"
        return footer_template.format(note.formatted_tags())

    def selectable(self):
        return True

    def is_high_priority(self):
        return self.note.priority >= 10


class NotesFrame(Frame):
    """"Frame for displaying notes and status"""

    def __init__(self, notes):
        note_widgets = self._create_note_widgets(notes)
        self.notes = NotesListBox(note_widgets)
        self.notes.focus_first()
        self.status = self._create_statusbar(notes)
        Frame.__init__(self, self.notes, footer=self.status)

    def _create_note_widgets(self, notes):
        note_widgets = []
        for note in notes:
            note_widgets.append(AttrMap(NoteWidget(note),
                                        None,
                                        'highlight_note'))
        return note_widgets

    def _create_statusbar(self, notes):
        aerende_text = Text("{0} :: {1}".format(title, version))
        notes_text = Text(" [ {0} ]".format(len(notes)), align='right')
        columns = Columns([aerende_text, notes_text])
        return AttrMap(Padding(columns, left=1, right=1), 'status_bar')

    def draw_notes(self, notes):
        notes.sort(key=lambda note: note.priority, reverse=True)
        note_widgets = self._create_note_widgets(notes)
        self.body.refresh_notes(note_widgets)
        self.footer = self._create_statusbar(notes)
        self.set_footer(self.footer)

    def show_note_editor(self, done_handler, note_to_edit=None):
        self.editor = AttrMap(NoteEditor(done_handler, note_to_edit),
                              'edit_bar')
        self.footer = self.editor
        self.set_footer(self.footer)
        self.set_focus('footer')

    def focus_next_note(self):
        self.body.focus_next()

    def focus_previous_note(self):
        self.body.focus_previous()

    def focus_first_note(self):
        self.body.focus_first()

    def get_focused_note(self):
        note_widget, _ = self.body.get_focus()
        return note_widget.original_widget.note


class TagsListBox(ListBox):
    """ListBox widget for displaying a list of tags"""

    def __init__(self, tags):
        tag_widgets = self._create_tag_widgets(tags)
        self.list_content = SimpleListWalker(tag_widgets)
        ListBox.__init__(self, self.list_content)

    def _create_tag_widgets(self, tags):
        tag_widgets = []
        for tag in tags:
            tag_widgets.append(Text(str(tag)))
        return tag_widgets

    def draw_tags(self, tags):
        tags.sort(key=lambda tag: tag.frequency, reverse=True)
        tag_widgets = self._create_tag_widgets(tags)
        self.list_content[:] = tag_widgets

    def get_max_width(self, tags):
        max_width = 30
        min_width = 18
        width = len(str(reduce((lambda x, y:
                                x if len(str(x)) > len(str(y)) else y),
                               tags))) + 2
        return max(min(max_width, width), min_width)


class NoteEditor(WidgetWrap):

    __metaclass__ = signals.MetaSignals
    signals = ['done']

    def __init__(self, done_handler, note=None):
        self.modes = ['title', 'tags', 'text']
        self.mode = self.modes[0]
        self.note = note
        if note is None:
            self.title = ''
            self.tags = ''
            self.text = ''
        else:
            self.title = note.title
            self.tags = note.formatted_tags()
            self.text = note.text

        self.editor = Edit(u'title :: ', self.title)
        connect_signal(self, 'done', done_handler)
        WidgetWrap.__init__(self, self.editor)

    def keypress(self, size, key):
        if key == 'enter':
            if self.mode == 'title':
                self.title = self.editor.get_edit_text()
                self.init_tags_mode()
            elif self.mode == 'tags':
                self.tags = self.editor.get_edit_text()
                self.init_text_mode()

        elif key == 'esc':
            self.emit_done()
            return

        size = size,
        self.editor.keypress(size, key)

    def init_tags_mode(self):
        self.mode = self.modes[1]
        self.editor.set_caption('tags :: ')
        self.editor.set_edit_text(self.tags)

    def init_text_mode(self):
        self.mode = self.modes[2]
        editor = os.environ.get('EDITOR', 'vim')
        with tempfile.NamedTemporaryFile(prefix="aerende_tmp",
                                         suffix=".tmp") as temp:
            temp.write(self.text.encode('utf-8'))
            temp.flush()
            call([editor, temp.name])
            temp.seek(0)
            self.text = temp.read().decode('utf-8').strip()
            os.system('clear')
            self.emit_done((self.title, self.tags, self.text))

    def emit_done(self, note=None):
        emit_signal(self, 'done', note, self.note)


class NotesListBox(ListBox):

    def __init__(self, contents):
        self.list_walker = SimpleListWalker(contents)
        ListBox.__init__(self, self.list_walker)

    def refresh_notes(self, notes):
        self.list_walker[:] = notes
        self.set_selected_style()

    def focus_next(self):
        _, position = self.get_focus()
        if position is None:
            return

        if position + 1 >= len(self.body):
            self.set_focus(position)
        else:
            self.set_focus(position + 1)
        self.set_selected_style()

    def focus_previous(self):
        _, position = self.get_focus()
        if position is None:
            return

        if position - 1 < 0:
            self.set_focus(position)
        else:
            self.set_focus(position - 1)
        self.set_selected_style()

    def focus_first(self):
        if len(self.body):
            self.set_focus(0)
            self.set_selected_style()

    def set_selected_style(self):
        focused, position = self.get_focus()
        if focused:
            focused.set_attr_map({None: 'highlight_note'})
        for object in self.body:
            if object is not focused:
                if object.original_widget.is_high_priority():
                    object.set_attr_map({None: 'high_priority'})
                else:
                    object.set_attr_map({None: None})
