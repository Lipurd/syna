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
from math import floor
import ssd1306

HEADLINE_MARGIN = const(16)

class Syna:

    def __init__(self, display, items, headline = None):

        # yellow header?
        self.headline = headline

        if self.headline:
            self.topmargin = HEADLINE_MARGIN
        else:
            self.topmargin = 0

        # display settings
        self.display = display
        self.height = display.height
        self.width = display.width

        # set maximum number of items per page
        self.pagebreak = int((self.height - self.topmargin) / 10 )

        self.items = items
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
            self.display.text(self.items[pos], 1, self.topmargin + (pos - (self.page * self.pagebreak))*10 + 1)

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

        self.display.framebuf.fill_rect(0, self.topmargin + (self.selected - (self.page * self.pagebreak))*10, self.width, 9, 1)
        self.display.text(self.items[self.selected], 1, self.topmargin + (self.selected - (self.page * self.pagebreak))*10 + 1, 0)

    def _deslect(self):
        """Reset the current 'on page position' menu item"""

        self.display.framebuf.fill_rect(0, self.topmargin + (self.selected - (self.page * self.pagebreak))*10, self.width, 9, 0)
        self.display.text(self.items[self.selected], 1, self.topmargin + (self.selected - (self.page * self.pagebreak))*10 + 1, 1)

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
