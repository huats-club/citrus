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

    # Method is invoked when the user clicks on "start" in Start page
    def on_start_button_press(self):

        # Get project settings from the Start page
        type_session, filepath = self.start.get_project_settings()

        # Valid user input from project settings
        is_valid_project_setting = (
            (filepath != "") and type_session == app_parameters.PROJECT_LOAD) or (
            type_session == app_parameters.PROJECT_NEW)

        # If valid project settings, then proceed to Main page
        if is_valid_project_setting:

            # Wipe out current window
            self.container.destroy()

            # Switch over to main page
            self.main_page = MainPage(self.view, self)  # parent of main page is root

        # If invalid project settings, then indicate error message
        else:
            # invalid
            self.start.display_error_message()
            return

    # Method is invoked when the app exits
    def on_exit(self):

        # Destroy entire window to exit
        print("Exiting...")
        self.view.destroy()
