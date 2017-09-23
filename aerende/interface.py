import urwid


class NoteWidget(urwid.LineBox):
    """Widget for displaying a note"""

    def __init__(self, note):
        self.note = note

        header = urwid.Text(self._create_header(note))
        footer = urwid.Text(self._create_footer(note))
        body = urwid.Filler(urwid.Text(note.text), 'top', top=1)

        frame = urwid.Padding(urwid.Frame(body, header=header, footer=footer),
                              left=1, right=1)

        urwid.LineBox.__init__(self, frame)


    def _create_header(self, note):
        return "{0} :: {1}".format(note.priority, note.title)


    def _create_footer(self, note):
        return str(note.tags)
