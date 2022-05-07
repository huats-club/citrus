import tkinter as tk
from view.start.start_page import StartPage
from view.main.main_page import MainPage
import config.app_parameters as app_parameters
from model.calibrate_handler import CalibrateHandler
from multiprocessing import Pipe


class Controller:
    def __init__(self, root):

        # Create tkinter container in root
        self.view = root
        self.container = tk.Frame(self.view)
        self.container.pack()

        # Create start page
        self.start = StartPage(self.container, self)

        # Flag to indicate if still calibrating
        self.is_calibrating = False

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

    # Method is called when any calibrate button is pressed
    # and stores the data in controller
    def on_calibrate(self, page):

        # Flag required to prevent double clicking
        if self.is_calibrating == False:

            # Indicate that calibrating
            self.is_calibrating = True

            # Disable calibration first
            page.disable_calibration()

            # Get reference to frequency setting pane of the page
            frequency_pane = page.get_frequency_setting_pane()

            # Get centre freq and bandwidth
            center_freq, bandwidth = frequency_pane.get_center_freq(), frequency_pane.get_bandwidth()

            # Get driver
            driver_name = page.get_driver_input()

            # Check if calibration can be done
            if center_freq == "" or bandwidth == "" or driver_name == "":

                # Set error message
                page.set_invalid_calibration_message()

                # Re-enable calibration
                page.enable_calibration()

                return

            print(f"Center freq: {center_freq}, bandwidth: {bandwidth}")

            # TODO: do calibration and feed back to page mode
            c = CalibrateHandler()
            self.pipe_here, pipe_calibrate = Pipe(True)
            c.start(driver_name, pipe_calibrate, center_freq, bandwidth, bandwidth)

            # Proceed to calibration polling method
            self.view.after(100, lambda: self.poll_calibrate(page))
            page.set_valid_calibration_message()

    def poll_calibrate(self, page):

        # Poll for incoming data and retrieve
        if self.pipe_here.poll(timeout=0):
            data = self.pipe_here.recv()
            self.calibrate_data = data
            self.is_calibrating = False

        if self.is_calibrating == True:
            self.view.after(50, lambda: self.poll_calibrate(page))

        else:
            # Display completed calibration message
            page.set_calibration_complete_message()

            # Indicate that calibrating stopped at the <END>
            self.is_calibrating = False

            # Re-enable calibration
            page.enable_calibration()

            print("complete spectrum mode calibration")
