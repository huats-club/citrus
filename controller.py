import tkinter as tk

import AppParameters as app_params
from view.main.MainPage import MainPage
from view.start.StartPage import StartPage


class Controller(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.parent.resizable(width=False, height=False)    # Don't allow resizing
        self.parent.title(app_params.APP_TITLE)
        self.parent.iconbitmap(app_params.APP_ICO_PATH)

        # Current session setting
        self.currentInterface = ""
        self.currentProjectSetting = ""

        # Put all pages into container
        self.container = tk.Frame(self.parent)
        self.container.pack()
        self.make_start_page()

    # Function to create start (landing) page
    def make_start_page(self):
        self.start = StartPage(self.container, self)

    # Function to execute when start button pressed
    def onStartButtonPress(self):
        isValidInterface = (self.start.getInterface() != "")
        isValidProjectSetting = (self.start.getProjectSetting() != "")

        # Valid user input
        if isValidInterface and isValidProjectSetting:
            print(self.start.getInterface(), self.start.getProjectSetting())
            self.currentInterface = self.start.getInterface()
            self.currentProjectSetting = self.start.getProjectSetting()

            # Wipe out current window
            self.container.destroy()

            # Add notebook to original
            self.make_main_page()

        else:  # invalid
            self.start.displayErrorMessage()
            return

    def make_main_page(self):
        self.main_page = MainPage(self.parent, self)  # parent of main page is root
