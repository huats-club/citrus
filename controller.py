import tkinter as tk
from multiprocessing import Pipe

import ezdxf

from app_parameters import app_parameters
from model.CoverageHandler import CoverageHandler
from model.PointsDataAggregator import PointDataAggregator
from model.PointsDataConverter import PointsDataConverter
from model.RecordingHandler import RecordingHandler
from model.WifiScanner import WifiScanner
from view.main.MainPage import MainPage
from view.start.StartPage import StartPage


class Controller(tk.Frame):
    def __init__(self, parent, session):
        super().__init__(parent)
        self.parent = parent
        self.parent.resizable(width=False, height=False)    # Don't allow resizing
        self.parent.title(app_parameters.APP_TITLE)
        self.parent.iconbitmap(app_parameters.APP_ICO_PATH)

        # Create new session object
        self.session = session

        # Create pipes for coverage process
        pipe_spectrum_process, pipe_spectrum_gui = Pipe(True)
        self.pipe_spectrum_process = pipe_spectrum_process
        self.pipe_spectrum_gui = pipe_spectrum_gui

        # Create pipes for recording process
        pipe_recording_process, pipe_recording_gui = Pipe(True)
        self.pipe_recording_process = pipe_recording_process
        self.pipe_recording_gui = pipe_recording_gui

        # Put all pages into container
        self.container = tk.Frame(self.parent)
        self.container.pack()
        self.make_start_page()

        # State variables
        self.is_spectrum_start = False
        self.is_recording_start = False

        # Reset dxf load variable
        self.dxf_opened = False

        # Scan results done
        self.scan_done = False

        # # Current wifi log
        # ts = datetime.datetime.date(datetime.datetime.now())
        # self.log_name = fr"{self.session.get_session_workspace_path()}/log_{ts}.txt"
        # self.log_json = fr"{self.session.get_session_workspace_path()}/{ts}.txt"

    # Function to create start (landing) page
    def make_start_page(self):
        self.start = StartPage(self.container, self)

    # Function to execute when start button pressed
    def on_start_button_press(self):
        type_session, filepath = self.start.get_project_settings()

        # Valid user input
        is_valid_project_setting = (
            (filepath != "") and type_session == app_parameters.PROJECT_LOAD) or (
            type_session == app_parameters.PROJECT_NEW)
        if is_valid_project_setting:

            # Wipe out current window
            self.container.destroy()

            # Add notebook to original
            self.make_main_page(self.pipe_spectrum_gui, self.pipe_recording_gui)

            # TODO: Set all the required if it is load
            if type_session == app_parameters.PROJECT_LOAD:
                pass

        else:  # invalid
            self.start.display_error_message()
            return

    def make_main_page(self, spectrum_pipe, recording_pipe):
        self.main_page = MainPage(self.parent, self, spectrum_pipe, recording_pipe,
                                  self.session)  # parent of main page is root

    def start_spectrum_process(self, driver_name, center_freq, bandwidth):
        # Create sdr handler
        self.sdr_handler = CoverageHandler(driver_name)
        self.sdr_handler.start(self.pipe_spectrum_process, center_freq, bandwidth)

    def stop_spectrum_process(self):
        self.sdr_handler.stop()

    def start_recording_process(self, driver_name, center_freq, bandwidth):
        self.recording_handler = RecordingHandler(driver_name)
        self.recording_handler.start(self.pipe_recording_process, center_freq, bandwidth)

    def stop_recording_process(self):
        self.recording_handler.stop()

    def load_dxf_to_canvas(self):

        if self.dxf_opened == False:
            self.dxf_filepath, self.dxf_filename = self.main_page.coverage_page.coverage_file_menu.get_dxf_filepath_selected()

            # remove extensions from dxf filename
            self.dxf_filename = self.dxf_filename.replace(".dxf", "")

            # Save filename into session
            self.session.save_dxf_name(self.dxf_filename)

            try:
                dxf = ezdxf.readfile(self.dxf_filepath)

                # Save file as class member
                self.dxf = dxf

            except IOError:
                self.main_page.coverage_page.set_load_dxf_error_message()
                return

            except ezdxf.DXFStructureError:
                self.main_page.coverage_page.set_load_dxf_error_message()
                return

            # Display dxf file
            self.main_page.coverage_page.display_dxf(self.dxf)

            # Flag to indicate dxf already opened
            self.dxf_opened = True

            # Cache the image of display on tkinter canvas after display
            # This is to create an image to etch up to tkinter canvas
            self.loaded_floorplan_saved_image_path = fr"{self.session.get_session_private_folder_path()}\{self.dxf_filename}_tkinter.png"
            self.main_page.coverage_page.after(
                500,
                lambda: self.main_page.coverage_page.capture_canvas(self.loaded_floorplan_saved_image_path)
            )

            # Enable plotting of points
            self.main_page.coverage_page.enable_canvas_click()

        else:
            self.main_page.coverage_page.disable_canvas_click()

    def clear_dxf_from_canvas(self):
        if self.dxf_opened == True:
            self.main_page.coverage_page.coverage_canvas.delete("all")
            self.dxf_opened = False

            self.main_page.coverage_page.clear_wifi_scan_results()

            # Disable canvas click
            self.main_page.coverage_page.disable_canvas_click()

        else:
            return

    def get_floorplan_image_path(self):
        return self.loaded_floorplan_saved_image_path

    def do_coverage_wifi_scan(self):

        # clear scan first
        self.main_page.coverage_page.clear_wifi_scan_results()

        # Do scan only if dxf is opened
        if self.dxf_opened:

            if self.scan_done:
                self.main_page.coverage_page.clear_wifi_scan_results()
                self.scan_done = False

            wifi_scanner = WifiScanner()
            results = wifi_scanner.scan()

            # if only one or none wifi then scan again
            if len(results) == 1 or len(results) == 2 or len(results) == 0:
                results = wifi_scanner.scan()

            self.main_page.coverage_page.populate_wifi_scan_results(results)

            # Indicate scan is done
            self.scan_done = True

        # Else, prompt dxf to be loaded
        else:
            self.main_page.coverage_page.set_no_dxf_error_message()

    # Save whatever plot is on the tkinter if valid heatmap
    def save_heatmap_plot(self, output_path, data, forceSave=False):

        status = False

        if self.session.is_need_to_save() or forceSave:

            # Display only if dxf file opened and wifi scan done
            if self.dxf_opened and self.scan_done:
                status = self.main_page.coverage_page.save_heatmap_plot(output_path, data)
                print("Scan done and dxf open")

            elif not self.dxf_opened:
                self.main_page.coverage_page.coverage_info_panel.set_no_dxf_error_message()
                print("dxf not open")
                status = False

            elif not self.scan_done:
                self.main_page.coverage_page.coverage_info_panel.set_no_wifi_scan_error_message()
                print("scan not done")
                status = False

            if not forceSave:
                self.session.set_no_need_to_save()

        return status

    # Generate and display created heatmap on tkinter canvas
    def display_heatmap(self):

        if self.session.is_need_to_save():

            # Now, all data is encapsulated in dict: (x,y)->Point objects
            # Use converter to convert all Points object to format for use
            points = self.main_page.coverage_page.get_points()

            converter = PointsDataConverter(points)
            processed_all_data = converter.process()

            # create a combined heatmap and add to map
            aggregator = PointDataAggregator(points)
            combined_heatmap_data = aggregator.process()
            processed_all_data['Combined'] = combined_heatmap_data

            # map (ssid)->(path)
            self.map_ssid_path = {}

            for ssid, data in processed_all_data.items():

                # generate name of path
                output_file_name = f"{self.session.get_dxf_prefix()}_{ssid}_{self.session.get_current_coverage_plot_num()}.png"

                # Don't save entire path into coverage, so that easier to handle load session
                saved_heatmap_path = f"{self.session.get_session_private_folder_relative_path()}/{output_file_name}"

                self.session.increment_coverage_plot_num()

                # save to map
                self.map_ssid_path[ssid] = saved_heatmap_path

                status = self.save_heatmap_plot(saved_heatmap_path, data, True)

                if status == False:
                    return

            # Set no need to save
            self.session.set_no_need_to_save()

        else:
            return

        # Save map to coverage
        self.main_page.coverage_page.set_ssid_heatmap_path(self.map_ssid_path)

        # Etch and populate all saved files onto menu
        if self.session.get_prev_coverage_plot_num() > 0:
            first_ssid_to_plot = list(self.map_ssid_path.keys())[0]

        else:
            first_ssid_to_plot = ""

        self.main_page.coverage_page.put_image(first_ssid_to_plot)

    def isValid(self):
        return self.dxf_opened and self.scan_done

    def set_scan_done(self):
        self.scan_done = True

    def set_scan_not_done(self):
        self.scan_done = False

    def on_exit(self, root):

        # NOTE: differentiated saving measures/algo for new/load session!!
        coverage = self.main_page.coverage_page
        session = self.main_page.coverage_page.session

        # TODO: save coverage window
        # for now, to process the strings, print out all fields that need to be saved
        print(f"paths: {session.get_relative_paths()}")
        print(f"{coverage.map_ssid_heatmap_path}")

        # Debug
        print("Exiting...")

        # Destroy entire window after completed saving session
        root.destroy()
