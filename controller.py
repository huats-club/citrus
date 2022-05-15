import tkinter as tk
from multiprocessing import Pipe
from tkinter import filedialog as tkfd

import ezdxf
import numpy as np

import config.app_parameters as app_parameters
from model.calibrate_handler import CalibrateHandler
from model.file_name_utils import FileNameUtil
from model.sdr_handler import SDRHandler
from model.wifi_handler import WifiHandler
from model.wifi_scanner import WifiScanner
from model.wifi_utils import WifiUtils
from view.main.main_page import MainPage
from view.main.recording.recording import RecordingPage
from view.main.spectrum.spectrum import SpectrumPage
from view.start.start_page import StartPage


class Controller:
    def __init__(self, root, session):

        # Create tkinter container in root
        self.view = root
        self.container = tk.Frame(self.view)
        self.container.pack()

        # Create start page
        self.start = StartPage(self.container, self)

        # Main page is None now
        self.main_page = None

        # Session object
        self.session = session

        # Flag to indicate if still calibrating
        self.is_calibrating = False

        # Store calibrate data
        self.calibrate_data = None

        # Flag to indicate if spectrum is start
        self.is_spectrum_start = False

        # Flag to indicate if recording is start
        self.is_recording_start = False

        # Mapping of bssid to Wifi entry object
        self.bssid_wifi_entry_mapping = {}
        self.has_wifi_scanned = False

        # Store wifi and points
        self.map_coord_wifi_entries = {}

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
            self.main_page = MainPage(self.view, self, self.session)  # parent of main page is root

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

            # Disable toggle to other tab
            self.main_page.disable_toggle_tab()

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

                # Enable toggle to other tab
                self.main_page.enable_toggle_tab()

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

            # Disable toggle to other tab
            self.main_page.enable_toggle_tab()

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

    # Method is invoked when recording starts
    def on_recording_start(self, recording_page):

        if self.is_recording_start == True:

            frequency_pane = recording_page.get_frequency_setting_pane()
            frequency_pane.display_error_message(True)
            recording_page.disable_start()
            self.is_recording_start = True

        elif self.is_recording_start == False:

            self.is_recording_start = True
            recording_page.disable_start()

            # If no calibrate data or deleted, display error message
            if self.calibrate_data == None:
                recording_page.set_missing_calibration_on_start_message()
                recording_page.enable_start()
                self.is_recording_start = False
                return

            # Retrieve frequency and bandwidth pane
            frequency_pane = recording_page.get_frequency_setting_pane()

            # Get centre freq and bandwidth
            center_freq, bandwidth = frequency_pane.get_center_freq(), frequency_pane.get_bandwidth()
            start_freq_string, end_freq_string = frequency_pane.get_start_freq(), frequency_pane.get_stop_freq()
            units = frequency_pane.get_freq_units()

            # Get driver
            driver_name = recording_page.get_driver_input()

            # Check if spectrum start can be done
            if center_freq == "" or bandwidth == "" or driver_name == "":

                # Set error message
                frequency_pane.display_error_message(False)

                # Re-enable spectrum start button
                recording_page.enable_start()

                return

            # Disable toggle to other tab
            self.main_page.disable_toggle_tab()

            # Disable setting of frequency in frequency pane
            frequency_pane.disable_frequency_pane()

            print(
                f"start freq | center freq | end freq | {start_freq_string} {center_freq} {end_freq_string} | {units} | bandwidth: {bandwidth}")

            # Begin sdr handler
            self.sdr_handler = SDRHandler(driver_name)
            self.sdr_handler.start(center_freq, bandwidth, bandwidth)
            data_pipe = self.sdr_handler.get_output_pipe()

            # Proceed to polling method for spectrum
            self.view.after(100, lambda: self.poll_recording(recording_page, self.sdr_handler, data_pipe))

    def poll_recording(self, recording_page, sdr_handler, data_pipe):

        # Poll for incoming data and retrieve
        if self.is_recording_start == True and data_pipe.poll(timeout=0):
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
            recording_page.do_plot(x)

        if self.is_recording_start == True:
            self.view.after(50, lambda: self.poll_recording(recording_page, sdr_handler, data_pipe))

    # Method is invoked when recording stops
    def on_recording_stop(self, recording_page):

        if self.is_recording_start == True:
            self.is_recording_start = False
            self.sdr_handler.stop()
            self.sdr_handler = None
            recording_page.enable_start()
            # Enable toggle to other tab
            self.main_page.enable_toggle_tab()

    # Method is invoked when save button is clicked
    def on_save(self, page, dirname):
        name = "citrus"
        if isinstance(page, RecordingPage):
            name = "recording"
        elif isinstance(page, SpectrumPage):
            name = "spectrum"
        image_fp = FileNameUtil.createFilepath(dirname, name, self.session.get_uuid())
        print(f"Saving recording image to {image_fp}")
        page.save_plot(image_fp)

    # Method is invoked when Select button is clicked on coverage
    def on_coverage_floorplan_select(self, coverage):
        try:
            path = tkfd.askopenfilename(
                initialdir="C:/", filetypes=(("dxf files", "*.dxf"),
                                             ("all files", "*.*")))
            coverage.set_floorplan_filepath_display(path)
        except ValueError:
            coverage.set_floorplan_filepath_display("")

    # Method is invoked when Load button is clicked on coverage
    def on_coverage_floorplan_load(self, coverage, filepath):
        try:
            dxf = ezdxf.readfile(filepath)
            print(f"Opened file: {filepath}")

        except IOError:
            coverage.set_load_dxf_error_message()
            return

        except ezdxf.DXFStructureError:
            coverage.set_load_dxf_error_message()
            return

        coverage.draw_dxf(dxf)

        # Strip filepath to filename only
        filename = filepath.split("/")[-1].replace(".dxf", "")

        # Cache the image of display on tkinter canvas after display
        # This is to create an image to etch up to tkinter canvas
        loaded_floorplan_saved_image_path = fr"{self.session.get_relative_private_path()}\{filename}_tkinter.png"
        print(f"Saving cached floorplan to {loaded_floorplan_saved_image_path}")
        coverage.after(500, lambda: coverage.capture_canvas(loaded_floorplan_saved_image_path))
        self.session.set_cached_floorplan_path(loaded_floorplan_saved_image_path)

        # Enable canvas click
        coverage.enable_canvas_click()

    # Method is invoked when clear button is clicked on coverage
    def on_coverage_floorplan_clear(self, coverage):
        # Clear canvas
        coverage.clear_canvas()

        # Disable canvas click
        self.main_page.coverage_page.disable_canvas_click()

    # Method is invoked when scan for available wifi
    def on_coverage_wifi_scan(self, coverage):
        if self.has_wifi_scanned == False:
            self.has_wifi_scanned = True

            wifi_scanner = WifiScanner()
            results = wifi_scanner.scan()

            # if only one or none wifi then scan again
            if len(results) == 1 or len(results) == 2 or len(results) == 0:
                results = wifi_scanner.scan()
                results = wifi_scanner.scan()

            # Populate mapping
            for entry in results:
                self.bssid_wifi_entry_mapping[entry.bssid] = entry

            # Populate to list of wifi
            print(f"Scanned: {results}")
            coverage.populate_scanned_wifi_list(results)

            # Enable click to add point
            coverage.enable_canvas_click()

    # Method is invoked when clear wifi scanned list
    def on_coverage_wifi_clear(self, coverage):
        coverage.on_coverage_wifi_clear()
        self.has_wifi_scanned = False

        # Disable click to add point
        coverage.disable_canvas_click()

    # Method is invoked when point is clicked and added to canvas
    def on_coverage_put_point(self, event, coverage):

        # If false, skip add point
        if self.has_wifi_scanned == False:
            return

        # Get signal (sdr/wifi) from point
        if coverage.get_current_signal_tab() == "WIFI":

            # Get list of bssid to track
            tracked_list_bssid = coverage.get_wifi_tracked_bssid_list()
            print(f"Tracking bssids: {tracked_list_bssid}")

            pipe_handler, pipe_here = Pipe(True)
            WifiHandler(tracked_list_bssid, pipe_handler).start()
            isRun = True
            while isRun:
                if pipe_here.poll(timeout=0):
                    wifi_entry_list = pipe_here.recv()
                    break

            print(f"Found: {wifi_entry_list}")
            coverage.add_point(event.x, event.y, WifiUtils.hovertext(wifi_entry_list))

            # Store in mapping
            self.map_coord_wifi_entries[(event.x, event.y)] = wifi_entry_list

        else:
            pass
