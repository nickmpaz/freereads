import curses
from .curses_components import *      
    
class ScrollPage(ScrollPageComponent):

    def __init__(self, height, width, begin_y, begin_x):
        super().__init__(height, width, begin_y, begin_x)
        self.focus = -1

    def decrement_focus(self):
        if self.focus > -1:
            self.focus -= 1
            return True
        else:
            return False

    def draw_item(self, row, item_index):

        row_content = self.items[item_index]['title']
        row_content = row_content.ljust(self.width - 1)

        if item_index == self.focus:
            self.win.addnstr(row, 0, row_content, self.width, curses.A_STANDOUT)
        else:
            self.win.addnstr(row, 0, row_content, self.width)

        self.win.clrtoeol()

class TextBox(TextBoxComponent):

    def __init__(self, height, width, begin_y, begin_x):
        super().__init__(height, width, begin_y, begin_x)
        self.content = {}

    def draw(self):
        for i, key in enumerate([
            "id",
            "author",
            "title",
            "md5",
            "publisher",
            "year",
            "pages",
            "language",
            "size",
            "extension"
        ]):
            self.win.addstr(i, 0, key + ": " + self.content.get(key, ""))
            self.win.clrtoeol()

        self.win.refresh()