import tkinter as tk

import AppParameters as app_params
from view.start.StartPage import StartPage


class Controller(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.parent.resizable(width=False, height=False)    # Don't allow resizing
        self.parent.title(app_params.APP_TITLE)
        self.parent.iconbitmap(app_params.APP_ICO_PATH)

        # Put all pages into container
        self.container = tk.Frame(self.parent)
        self.container.pack()
        self.make_start_page()

    # Function to create start (landing) page
    def make_start_page(self):
        self.start = StartPage(self.container, self)

    # Function to execute when start button pressed
    def onStartButtonPress(self):
        print("Start page's start button pressed")
        print(self.start.project_frame.getSelection())
