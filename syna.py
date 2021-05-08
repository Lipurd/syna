##################################################
## syna.py
## Menu assistant for SSD1306 Displays
## on ESP32 and ESP8266
##################################################
## Author: Dustin Kröger
## Copyright: Copyright 2021, Lipurd
## License: MIT License
## Version: 0.1.0
##################################################

from micropython import const

HEADLINE_MARGIN = const(16)

class SynaInterface:

    def __init__(self, headline = None, parent = None):
        self.headline = headline
        self.parent = parent
        pass

    def show(self):
        pass
    def up(self):
        pass
    def down(self):
        pass
    def click(self):
        pass

class Syna(SynaInterface):

    def __init__(self, display):
        self.display = display
        self.views = {}
        self.view = None

    def addMenu(self, identifier, items, headline = None, parent = None):

        self.views[identifier] = Menu(self.display, items, headline, parent)
        self.views[identifier].identifier = identifier

    def addView(self, identifier, view, headline = None, parent = None):

        self.views[identifier] = view(headline, parent)
        self.views[identifier].identifier = identifier

    def show(self, identifier):

        self.view = self.views[identifier]
        self.view.show()

    def click(self):

        # check if menu with list as item
        if isinstance(self.view, Menu):
            if isinstance(self.view.items[self.view.selected], list):
                itemstr = self.view.items[self.view.selected][1]
                if itemstr[:1] == '@':
                    self.show(itemstr[1:])

        self.view.click()

    def down(self):

        self.view.down()

    def up(self):

        self.view.up()


class Menu(SynaInterface):

    def __init__(self, display, items, headline = None, parent = None):

        super().__init__(headline, parent)
        self.items = items

        # add back to parent
        if self.parent:
            self.items.append(['back', '@%s' % self.parent])

        self.display = display

        # set headline
        if self.headline:
            self.topmargin = HEADLINE_MARGIN
        else:
            self.topmargin = 0

        # set maximum number of items per page
        self.pagebreak = int((self.display.height - self.topmargin) / 10 )

        self.selected = 0
        self.page = 0
        self.nextpagestr = None

    def show(self):
        """Display the menu items on the current page"""

        # clear screen
        self.display.fill(0)

        # print headline if set (margin gets set by init)
        # also reset margin if value changed after init
        if self.headline:
            self.topmargin = HEADLINE_MARGIN
            self.display.text(self.headline, 0, 0)
        else:
            self.topmargin = 0

        # add menu items per page
        for pos in range(self.page * self.pagebreak, len(self.items)):

            # print menu item with the current "on page position" + 1 + headline margin
            self.display.text(self._itemtext(pos), 1, self.topmargin + (pos - (self.page * self.pagebreak))*10 + 1)

            # check if next item would be out of bound
            if (pos - (self.page * self.pagebreak) + 1) >= self.pagebreak:

                # print dots or other str in last row
                if self.nextpagestr:
                    self.display.text(self.nextpagestr, 1, self.topmargin + self.pagebreak*10 + 1)
                break

        # highlight current item
        self._select()
        self.display.show()

    def _select(self):
        """Highlight the current 'on page position' menu item"""

        self.display.framebuf.fill_rect(0, self.topmargin + (self.selected - (self.page * self.pagebreak))*10, self.display.width, 9, 1)
        self.display.text(self._itemtext(self.selected), 1, self.topmargin + (self.selected - (self.page * self.pagebreak))*10 + 1, 0)

    def _deslect(self):
        """Reset the current 'on page position' menu item"""

        self.display.framebuf.fill_rect(0, self.topmargin + (self.selected - (self.page * self.pagebreak))*10, self.display.width, 9, 0)
        self.display.text(self._itemtext(self.selected), 1, self.topmargin + (self.selected - (self.page * self.pagebreak))*10 + 1, 1)

    def _itemtext(self, pos):

        if isinstance(self.items[pos], list):
            return str(self.items[pos][0])

        return str(self.items[pos])

    def click(self):
        """Click on a menu item"""

        # abort if no call specified
        if not isinstance(self.items[self.selected], list) or len(self.items[self.selected]) != 2:
            return

        eval(self.items[self.selected][1])

    def down(self):
        """Navigate down in the menu"""

        self._deslect()

        if (self.selected + 1) == len(self.items):
            self.selected = 0
            self.page = 0
            self.show()
            return

        else:
            self.selected += 1

        if self.selected == ((self.page + 1) * self.pagebreak):
            self.page += 1
            self.show()
            return

        self._select()
        self.display.show()

    def up(self):
        """Navigate up in the menu"""

        self._deslect()

        # check if already the top item, if yes, set to last
        if self.selected is 0:
            # set to last page
            self.page = int((len(self.items) -1)  / self.pagebreak)
            # set to last item
            self.selected = (len(self.items) - 1)
            self.show()
            return

        # check if current item is top on page and is changing to the prior page
        elif self.selected == (self.page * self.pagebreak):
            self.page -= 1
            self.selected -= 1
            self.show()
            return

        else:
            self.selected -= 1

        self._select()
        self.display.show()
