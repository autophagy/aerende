import urwid


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
