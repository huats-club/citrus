import tkinter as tk
from multiprocessing import Pipe

import numpy as np

import config.app_parameters as app_parameters
from model.calibrate_handler import CalibrateHandler
from model.sdr_handler import SDRHandler
from view.main.main_page import MainPage
from view.start.start_page import StartPage


class Controller:
    def __init__(self, root):

        # Create tkinter container in root
        self.view = root
        self.container = tk.Frame(self.view)
        self.container.pack()

        # Create start page
        self.start = StartPage(self.container, self)

        # Main page is None now
        self.main_page = None

        # Flag to indicate if still calibrating
        self.is_calibrating = False

        # Store calibrate data
        self.calibrate_data = None

        # Flag to indicate if spectrum is start
        self.is_spectrum_start = False

    # Method is invoked when main page tab is switched
    def on_tab_change(self, event):
        # NOTE: Need to differentiate and store calibrate data per tab separately?
        self.is_calibrating = False
        self.calibrate_data = None

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

                self.is_calibrating = False

                return

            print(f"Center freq: {center_freq}, bandwidth: {bandwidth}")

            # Do calibration
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

    # Method is invoked when spectrum starts
    def on_spectrum_start(self, spectrum_page):

        if self.is_spectrum_start == True:

            frequency_pane = spectrum_page.get_frequency_setting_pane()
            frequency_pane.display_error_message(True)
            spectrum_page.disable_start()
            self.is_spectrum_start = True

        elif self.is_spectrum_start == False:

            self.is_spectrum_start = True
            spectrum_page.disable_start()

            # If no calibrate data or deleted, display error message
            if self.calibrate_data == None:
                spectrum_page.set_missing_calibration_on_start_message()
                spectrum_page.enable_start()
                self.is_spectrum_start = False
                return

            # Retrieve frequency and bandwidth pane
            frequency_pane = spectrum_page.get_frequency_setting_pane()

            # Get centre freq and bandwidth
            center_freq, bandwidth = frequency_pane.get_center_freq(), frequency_pane.get_bandwidth()
            start_freq_string, end_freq_string = frequency_pane.get_start_freq(), frequency_pane.get_stop_freq()
            units = frequency_pane.get_freq_units()

            # Get driver
            driver_name = spectrum_page.get_driver_input()

            # Check if spectrum start can be done
            if center_freq == "" or bandwidth == "" or driver_name == "":

                # Set error message
                frequency_pane.display_error_message(False)

                # Re-enable spectrum start button
                spectrum_page.enable_start()

                return

            # Disable toggle to other tab
            self.main_page.disable_toggle_tab()

            # Disable setting of frequency in frequency pane
            frequency_pane.disable_frequency_pane()

            print(
                f"start freq | center freq | end freq | {start_freq_string} {center_freq} {end_freq_string} | {units} | bandwidth: {bandwidth}")

            # Setup x-axis
            spectrum_page.setup_plot_axis(start_freq_string, center_freq, end_freq_string, units)

            # Begin sdr handler
            self.sdr_handler = SDRHandler(driver_name)
            self.sdr_handler.start(center_freq, bandwidth, bandwidth)
            data_pipe = self.sdr_handler.get_output_pipe()

            # Proceed to polling method for spectrum
            self.view.after(100, lambda: self.poll_spectrum(spectrum_page, self.sdr_handler, data_pipe))

    def poll_spectrum(self, spectrum_page, sdr_handler, data_pipe):

        # Poll for incoming data and retrieve
        if self.is_spectrum_start == True and data_pipe.poll(timeout=0):
            data = data_pipe.recv()

            average_of_all_calibrate = np.average(data)
            data = np.subtract(data, self.calibrate_data)
            data = data + average_of_all_calibrate

            # do plot
            x = data.tolist()

            for idx in range(len(x)):
                if x[idx] < 0:
                    x[idx] = average_of_all_calibrate

            # do plot
            spectrum_page.do_plot(x)

        if self.is_spectrum_start == True:
            self.view.after(50, lambda: self.poll_spectrum(spectrum_page, sdr_handler, data_pipe))

    # Method is invoked when spectrum starts
    def on_spectrum_stop(self, spectrum_page):

        if self.is_spectrum_start == True:
            self.is_spectrum_start = False
            self.sdr_handler.stop()
            self.sdr_handler = None
            spectrum_page.enable_start()
            # Enable toggle to other tab
            self.main_page.enable_toggle_tab()
