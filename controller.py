import tkinter as tk
from multiprocessing import Pipe

from app_parameters import app_parameters
from model.SDRHandler import SDRHandler
from view.main.MainPage import MainPage
from view.start.StartPage import StartPage


class Controller(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.parent.resizable(width=False, height=False)    # Don't allow resizing
        self.parent.title(app_parameters.APP_TITLE)
        self.parent.iconbitmap(app_parameters.APP_ICO_PATH)

        # Create pipes for process
        pipe_process, pipe_gui = Pipe(True)
        self.pipe_process = pipe_process
        self.pipe_gui = pipe_gui

        # Put all pages into container
        self.container = tk.Frame(self.parent)
        self.container.pack()
        self.make_start_page()

        # State variables
        self.is_spectrum_start = False

    # Function to create start (landing) page
    def make_start_page(self):
        self.start = StartPage(self.container, self)

    # Function to execute when start button pressed
    def on_start_button_press(self):
        is_valid_interface = (self.start.get_interface() != "")
        is_valid_project_setting = (self.start.get_project_settings() != "")

        # Valid user input
        if is_valid_interface and is_valid_project_setting:
            print(self.start.get_interface(), self.start.get_project_settings())
            self.current_interface = self.start.get_interface()
            self.is_valid_project_setting = self.start.get_project_settings()

            # Wipe out current window
            self.container.destroy()

            # Add notebook to original
            self.make_main_page(self.pipe_gui)

        else:  # invalid
            self.start.display_error_message()
            return

    def make_main_page(self, data_pipe):
        self.main_page = MainPage(self.parent, self, data_pipe)  # parent of main page is root

    def start_spectrum_process(self, center_freq):
        # Create sdr handler
        self.sdr_handler = SDRHandler()
        self.sdr_handler.start(self.pipe_process, center_freq)

    def stop_spectrum_process(self):
        self.sdr_handler.stop()

    def load_dxf_to_canvas(self):
        print(self.main_page.coverage_page.coverage_file_menu.get_dxf_filepath_selected())
        pass
