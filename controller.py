import math
import os
import tkinter as tk
from multiprocessing import Pipe
from tkinter import filedialog as tkfd

import ezdxf
import numpy as np

import config.app_parameters as app_parameters
from model.calibrate_handler import CalibrateHandler
from model.coverage_handler import CoverageSingleHandler
from model.file_name_utils import FileNameUtil
from model.sdr_entry import SdrEntry
from model.sdr_handler import SDRHandler
from model.sdr_result_aggregator import SdrResultAggregator
from model.sdr_results_converter import SdrResultsConverter
from model.sdr_utils import SdrUtils
from model.wifi_entry import WifiEntry
from model.wifi_handler import WifiHandler
from model.wifi_heatmap_plotter import WifiHeatmapPlotter
from model.wifi_result_aggregator import WifiResultAggregator
from model.wifi_results_converter import WifiResultsConverter
from model.wifi_scanner import WifiScanner
from model.wifi_utils import WifiUtils
from view.main.main_page import MainPage
from view.main.recording.recording import RecordingPage
from view.main.spectrum.spectrum import SpectrumPage
from view.start.start_page import StartPage


# This is a controller for Citrus app
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

        # Store sdr and points
        self.map_coord_sdr_entries = {}

        # map (bssid)->(path) for coverage mode
        self.map_name_path = {}

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
            # Retrieve frequency and bandwidth pane
            frequency_pane = spectrum_page.get_frequency_setting_pane()
            # Disable setting of frequency in frequency pane
            frequency_pane.enable_frequency_pane()

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
            self.view.after(
                100, lambda: self.poll_recording(
                    recording_page, self.sdr_handler, data_pipe, int(start_freq_string),
                    center_freq, int(end_freq_string),
                    bandwidth))

    def poll_recording(self, recording_page, sdr_handler, data_pipe, start_freq, center_freq, end_freq, bandwidth):

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
            recording_page.do_plot(x, start_freq, center_freq, end_freq, bandwidth)

        if self.is_recording_start == True:
            self.view.after(50, lambda: self.poll_recording(
                recording_page, sdr_handler, data_pipe, start_freq, center_freq, end_freq, bandwidth))

    # Method is invoked when recording stops
    def on_recording_stop(self, recording_page):

        if self.is_recording_start == True:
            self.is_recording_start = False
            self.sdr_handler.stop()
            self.sdr_handler = None
            recording_page.enable_start()
            # Enable toggle to other tab
            self.main_page.enable_toggle_tab()
            # Retrieve frequency and bandwidth pane
            frequency_pane = recording_page.get_frequency_setting_pane()
            # Disable setting of frequency in frequency pane
            frequency_pane.enable_frequency_pane()

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
        self.session.set_dxf_prefix(filename)

        # Cache the image of display on tkinter canvas after display
        # This is to create an image to etch up to tkinter canvas
        loaded_floorplan_saved_image_path = fr"{self.session.get_relative_private_path()}\{filename}_tkinter.png"
        print(f"Saving cached floorplan to {loaded_floorplan_saved_image_path}")
        coverage.after(500, lambda: coverage.save_plot(loaded_floorplan_saved_image_path))
        self.session.set_cached_floorplan_path(loaded_floorplan_saved_image_path)

        # Enable canvas click
        coverage.enable_canvas_click()

    # Method is invoked when clear button is clicked on coverage
    def on_coverage_floorplan_clear(self, coverage):
        # Clear canvas
        coverage.clear_canvas()

        self.map_coord_wifi_entries.clear()
        self.bssid_wifi_entry_mapping = {}

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
            self.results_scan = results  # store results for querying later for lost signals
            coverage.populate_scanned_wifi_list(results)

            # Enable click to add point
            coverage.enable_canvas_click()

    # Method is invoked when clear wifi scanned list
    def on_coverage_wifi_clear(self, coverage):
        coverage.on_coverage_wifi_clear()
        self.map_coord_wifi_entries.clear()
        self.has_wifi_scanned = False
        self.bssid_wifi_entry_mapping = {}

        # Disable click to add point
        coverage.disable_canvas_click()

    # Method is invoked when point is clicked and added to canvas
    def on_coverage_put_point(self, event, coverage):

        # Get signal (sdr/wifi) from point
        if coverage.get_current_signal_tab() == "WIFI":

            tracked_list_bssid = coverage.get_wifi_tracked_bssid_list()
            print(f"tracked_list_bssid: {tracked_list_bssid}")

            # If no wifi scanned or no wifi entry chosen, skip add point
            if self.has_wifi_scanned == False or len(tracked_list_bssid) == 0:
                print("returning!")
                return

            # Get list of bssid to track
            print(f"Tracking bssids: {tracked_list_bssid}")

            wifi_scanner = WifiScanner(tracked_list_bssid)
            wifi_entry_list = wifi_scanner.scan()
            # pipe_handler, pipe_here = Pipe(True)
            # WifiHandler(tracked_list_bssid, pipe_handler).start()
            # isRun = True
            # while isRun:
            #     if pipe_here.poll(timeout=0):
            #         wifi_entry_list = pipe_here.recv()
            #         break

            if wifi_entry_list == [] or wifi_entry_list == None:
                print("Empty scanned list! Drop data point")
                return

            ##############################

            # Check if all wifi bssid entries
            for bssid in tracked_list_bssid:
                found = False
                for entry in wifi_entry_list:
                    # If scanned and found the strength, check the next
                    if bssid == entry.bssid:
                        found = True
                        break

                # Not found, add the entry
                if not found:
                    for x in self.results_scan:
                        if x.bssid == bssid:
                            print(f"Not found: {x.ssid}")
                            print(f"x: {x}")
                            wifi_entry_list += [WifiEntry(x.ssid, x.bssid, -100,  x.channel_frequency,
                                                          x.channel_number, x.channel_width)]

            ##############################

            print(f"At point ({event.x}, {event.y}): {wifi_entry_list}")
            coverage.add_point(event.x, event.y, WifiUtils.hovertext(wifi_entry_list))

            # Store in mapping
            self.map_coord_wifi_entries[(event.x, event.y)] = wifi_entry_list

        else:

            if self.calibrate_data == None:
                coverage.set_invalid_calibration_message()
                return

            sdr_tab = coverage.get_sdr_tab()
            tracked_freq_names = sdr_tab.get_tracked_map_name_freq()

            # store names and freqs
            names = []
            freqs = []

            # calculate best range
            bandwidth = 20e6
            min_freq = 100e9
            max_freq = 0

            for pair in tracked_freq_names:
                name, freq = list(pair.items())[0]
                names.append(name)
                freqs.append(freq)

                if freq > max_freq:
                    max_freq = freq

                if freq < min_freq:
                    min_freq = freq

            print(f"min freq: {min_freq}, max_freq: {max_freq}")
            scan_center_freq = (min_freq + max_freq) / 2
            driver = coverage.get_driver_input()
            c = CoverageSingleHandler(driver, self.calibrate_data)
            c.start(scan_center_freq, bandwidth, bandwidth)
            dbm_data = c.get_result()
            c.close()

            # track if each has freq to be tracked
            scan_freq_inc = bandwidth / len(dbm_data)
            start_freq = scan_center_freq - 0.5*bandwidth
            end_freq = scan_center_freq + 0.5*bandwidth
            print(f"start freq: {start_freq}, center_freq: {scan_center_freq}, end_freq: {end_freq}")
            print(f"freq increment: {scan_freq_inc:.5f}")

            # Pack into sdr result object
            sdr_entry_list = []
            for idx in range(len(freqs)):
                # compute idx to search
                located_center_idx = math.ceil((freqs[idx] - start_freq) / scan_freq_inc)
                left_bound_idx = located_center_idx - 1
                right_bound_idx = located_center_idx + 1

                # prevent out of bounds
                if left_bound_idx < 0:
                    left_bound_idx = 0
                if right_bound_idx > len(dbm_data):
                    right_bound_idx = len(dbm_data)

                print(f"searching: {left_bound_idx} -> {right_bound_idx}")

                # find the max dbm
                max_dbm_found = -100
                for idx2 in range(left_bound_idx, right_bound_idx+1):
                    if idx2 < len(dbm_data) and dbm_data[idx2] > max_dbm_found:
                        max_dbm_found = dbm_data[idx2]
                print(f"found max: {max_dbm_found:.5f}")

                sdr_entry_list.append(SdrEntry(names[idx], freqs[idx]/1e6, max_dbm_found))

            print(f"At point ({event.x}, {event.y}): {sdr_entry_list}")
            coverage.add_point(event.x, event.y, SdrUtils.hovertext(sdr_entry_list))
            self.map_coord_sdr_entries[(event.x, event.y)] = sdr_entry_list

    # Method is invoked when create heatmap is clicked
    def on_coverage_create(self, coverage):

        # Get signal (sdr/wifi) from point
        if coverage.get_current_signal_tab() == "WIFI":

            # If no coordinates, skip
            if len(self.map_coord_wifi_entries.keys()) == 0:
                return

            # map (ssid)->(path)
            self.map_name_path = {}

            processed_all_data = WifiResultsConverter(self.map_coord_wifi_entries).process()
            combined_result = WifiResultAggregator(self.map_coord_wifi_entries).process()
            processed_all_data['Combined'] = combined_result

            for name, result in processed_all_data.items():
                nametemp = name.replace(':', '')
                filename = f"{self.session.get_dxf_prefix()}_{self.session.get_uuid()}_{nametemp}.png"
                saved_heatmap_path = f"{self.session.get_relative_private_path()}/{filename}"
                saved_heatmap_path = saved_heatmap_path.replace(" ", "_")

                # save to map
                if name != "Combined":
                    ssid = self.bssid_wifi_entry_mapping[name].ssid
                    bssid = name
                    self.map_name_path[f"{ssid}{bssid}"] = saved_heatmap_path
                else:
                    self.map_name_path[f"Combined"] = saved_heatmap_path

                WifiHeatmapPlotter(result, self.session.get_cached_floorplan_path()).save(saved_heatmap_path)
                print(f"Creating {saved_heatmap_path}")

            # Set mapping in option menu for selection
            print("Storing map:")
            for name, path in self.map_name_path.items():
                print(f"\t{name} -> {path}")
            coverage.set_name_heatmap_path_mapping(self.map_name_path)

            # Set first image to plot
            points = list(self.map_coord_wifi_entries.keys())
            hovertexts = [WifiUtils.hovertext(entry) for entry in list(self.map_coord_wifi_entries.values())]
            coverage.put_image(list(self.map_name_path.values())[0], points, hovertexts)

        else:

            if self.calibrate_data == None:
                coverage.set_invalid_calibration_message()
                return

            # If no coordinates, skip
            if len(self.map_coord_sdr_entries.keys()) == 0:
                return

            # map (name)->(path)
            self.map_name_path = {}

            processed_all_data = SdrResultsConverter(self.map_coord_sdr_entries).process()
            combined_result = SdrResultAggregator(self.map_coord_sdr_entries).process()
            processed_all_data['Combined'] = combined_result

            for name, result in processed_all_data.items():
                nametemp = name.replace(':', '')
                filename = f"{self.session.get_dxf_prefix()}_{self.session.get_uuid()}_{nametemp}.png"
                saved_heatmap_path = f"{self.session.get_relative_private_path()}/{filename}"
                saved_heatmap_path = saved_heatmap_path.replace(" ", "_")

                # save to map
                if name != "Combined":
                    self.map_name_path[f"{name}"] = saved_heatmap_path
                else:
                    self.map_name_path[f"Combined"] = saved_heatmap_path

                WifiHeatmapPlotter(result, self.session.get_cached_floorplan_path()).save(saved_heatmap_path)
                print(f"Creating {saved_heatmap_path}")

            # Set mapping in option menu for selection
            print("Storing map:")
            for name, path in self.map_name_path.items():
                print(f"\t{name} -> {path}")
            coverage.set_name_heatmap_path_mapping(self.map_name_path)

            # Set first image to plot
            points = list(self.map_coord_sdr_entries.keys())
            hovertexts = [SdrUtils.hovertext(entry) for entry in list(self.map_coord_sdr_entries.values())]
            coverage.put_image(list(self.map_name_path.values())[0], points, hovertexts)

    def on_coverage_switch_heatmap(self, coverage, name):
        path = self.map_name_path[name]

        # Get signal (sdr/wifi) from point
        if coverage.get_current_signal_tab() == "WIFI":
            # Set first image to plot
            points = list(self.map_coord_wifi_entries.keys())
            hovertexts = [WifiUtils.hovertext(entry) for entry in list(self.map_coord_wifi_entries.values())]
            coverage.put_image(path, points, hovertexts)

        else:
            # Set first image to plot
            points = list(self.map_coord_sdr_entries.keys())
            hovertexts = [SdrUtils.hovertext(entry) for entry in list(self.map_coord_sdr_entries.values())]
            coverage.put_image(path, points, hovertexts)

    # Method is called when any calibrate button is pressed
    # and stores the data in controller
    def on_coverage_calibrate(self, coverage):
        # Flag required to prevent double clicking
        if self.is_calibrating == False:

            # Indicate that calibrating
            self.is_calibrating = True

            # Disable toggle to other tab
            self.main_page.disable_toggle_tab()

            # Disable calibration first
            coverage.disable_calibration()

            sdr_tab = coverage.get_sdr_tab()

            # Get centre freq and bandwidth
            center_freq, bandwidth = sdr_tab.get_center_freq(), sdr_tab.get_bandwidth()

            # Get driver
            driver_name = coverage.get_driver_input()

            # Check if calibration can be done
            if center_freq == "" or bandwidth == "" or driver_name == "":

                # Set error message
                coverage.set_invalid_calibration_message()

                # Re-enable calibration
                coverage.enable_calibration()

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
            self.view.after(100, lambda: self.poll_coverage_calibrate(coverage))
            coverage.set_valid_calibration_message()

    def poll_coverage_calibrate(self, coverage):

        # Poll for incoming data and retrieve
        if self.pipe_here.poll(timeout=0):
            data = self.pipe_here.recv()
            self.calibrate_data = data
            self.is_calibrating = False

        if self.is_calibrating == True:
            self.view.after(50, lambda: self.poll_calibrate(coverage))

        else:
            # Display completed calibration message
            coverage.set_calibration_complete_message()

            # Indicate that calibrating stopped at the <END>
            self.is_calibrating = False

            # Re-enable calibration
            coverage.enable_calibration()

            # Disable toggle to other tab
            self.main_page.enable_toggle_tab()

            # remove temp file
            os.remove("lswifi1.log")

            print("complete coverage mode calibration")
