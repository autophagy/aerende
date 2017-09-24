import urwid
from . import version, title


class NoteWidget(urwid.LineBox):
    """Widget for displaying a note"""

    def __init__(self, note):
        self.note = note

        header = self._create_header(note)
        footer = self._create_footer(note)
        note_display = urwid.Text("{0}\n\n{1}\n\n{2}".format(
                                  header, note.text, footer))
        urwid.LineBox.__init__(self, note_display)


    def _create_header(self, note):
        return "{0} :: {1}".format(note.priority, note.title)


    def _create_footer(self, note):
        footer_template = "[ {0} ]"
        return footer_template.format(" // ".join(note.tags))


class NotesFrame(urwid.Frame):
    """"Frame for displaying notes and status"""

    def __init__(self, notes):
        self.notes = notes

        note_widgets = []
        for note in notes:
            note_widgets.append(NoteWidget(note))

        self.notes_listbox = urwid.ListBox(urwid.SimpleListWalker(note_widgets))
        self.status = self._create_statusbar(notes)

        urwid.Frame.__init__(self, self.notes_listbox, footer=self.status)


    def _create_statusbar(self, notes):
        aerende_text = urwid.Text("{0} :: {1}".format(title, version))
        notes_text = urwid.Text(" [ {0} ]".format(len(notes)), align='right')
        columns = urwid.Columns([aerende_text, notes_text])
        return urwid.AttrMap(urwid.Padding(columns, left=1, right=1), 'highlight')
