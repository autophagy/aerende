from urwid import (Columns,
                   LineBox,
                   Text,
                   Frame,
                   ListBox,
                   AttrMap,
                   Padding,
                   SimpleListWalker)

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
        return footer_template.format(" // ".join(note.tags))


class NotesFrame(Frame):
    """"Frame for displaying notes and status"""

    def __init__(self, notes):
        note_widgets = self._create_note_widgets(notes)
        self.notes = ListBox(SimpleListWalker(note_widgets))
        self.status = self._create_statusbar(notes)
        Frame.__init__(self, self.notes, footer=self.status)

    def _create_note_widgets(self, notes):
        note_widgets = []
        for note in notes:
            note_widgets.append(NoteWidget(note))
        return note_widgets

    def _create_statusbar(self, notes):
        aerende_text = Text("{0} :: {1}".format(title, version))
        notes_text = Text(" [ {0} ]".format(len(notes)), align='right')
        columns = Columns([aerende_text, notes_text])
        return AttrMap(Padding(columns, left=1, right=1), 'highlight')

    def draw_notes(self, notes):
        note_widgets = self._create_note_widgets(notes)
        self.body = ListBox(SimpleListWalker(note_widgets))
        self.set_body(self.body)
        self.footer = self._create_statusbar(notes)
        self.set_footer(self.footer)


class TagsListBox(ListBox):
    """ListBox widget for displaying a list of tags"""

    def __init__(self, tags):
        tag_widgets = self._create_tag_widgets(tags)
        ListBox.__init__(self, SimpleListWalker(tag_widgets))

    def _create_tag_widgets(self, tags):
        tag_widgets = []
        for tag in tags:
            tag_widgets.append(Text(str(tag)))
        return tag_widgets

    def draw_tags(self, tags):
        tag_widgets = self._create_tag_widgets(tags)
        self.body = SimpleListWalker(tag_widgets)

    def get_max_width(self, tags):
        max_width = 30
        min_width = 18
        width = 0
        for tag in tags:
            l = len(str(tag)) + 2
            if l > width:
                width = l

        if width > max_width:
            return max_width
        elif width < min_width:
            return min_width
        return max_width
