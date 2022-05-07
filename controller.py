import tkinter as tk
from view.start.start_page import StartPage
from view.main.main_page import MainPage
import config.app_parameters as app_parameters


class Controller:
    def __init__(self, root):

        # Create tkinter container in root
        self.view = root
        self.container = tk.Frame(self.view)
        self.container.pack()

        # Create start page
        self.start = StartPage(self.container, self)

    def on_start_button_press(self):

        type_session, filepath = self.start.get_project_settings()

        # Valid user input
        is_valid_project_setting = (
            (filepath != "") and type_session == app_parameters.PROJECT_LOAD) or (
            type_session == app_parameters.PROJECT_NEW)

        if is_valid_project_setting:

            # Wipe out current window
            self.container.destroy()

            # Switch over to main page
            self.main_page = MainPage(self.view, self)  # parent of main page is root

        else:
            # invalid
            self.start.display_error_message()
            return

    def on_exit(self):

        # Destroy entire window to exit
        print("Exiting...")
        self.view.destroy()
