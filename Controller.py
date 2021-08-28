import tkinter as tk

import AppParameters as app_params
from view.start.landing import Landing


class Controller(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.parent.resizable(width=False, height=False)    # Don't allow resizing
        self.parent.title(app_params.APP_TITLE)
        self.parent.iconbitmap(app_params.APP_ICO_PATH)

        # Put all pages into container
        self.container = tk.Frame(self.parent)
        self.container.pack()
        self.make_landing_page()

    # Function to create start (landing) page
    def make_landing_page(self):
        self.landing = Landing(self.container, self)
