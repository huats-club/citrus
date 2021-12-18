import datetime as datetime
import tkinter as tk
from multiprocessing import Pipe

import ezdxf

from app_parameters import app_parameters
from model.CoverageHandler import CoverageHandler
from model.RecordingHandler import RecordingHandler
from model.Session import Session
from model.WifiScanner import WifiScanner
from view.main.MainPage import MainPage
from view.start.StartPage import StartPage


class Controller(tk.Frame):
    def __init__(self, parent, session_name):
        super().__init__(parent)
        self.parent = parent
        self.parent.resizable(width=False, height=False)    # Don't allow resizing
        self.parent.title(app_parameters.APP_TITLE)
        self.parent.iconbitmap(app_parameters.APP_ICO_PATH)

        # Create new session object
        self.session = Session(session_name)

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

        # Indicate current interface
        self.current_interface = app_parameters.INTERFACE_WIFI

        # Current wifi log
        ts = datetime.datetime.date(datetime.datetime.now())
        self.log_name = fr"{self.session.get_session_workspace_path()}/log_{ts}.txt"
        self.log_json = fr"{self.session.get_session_workspace_path()}/{ts}.txt"

    # Function to create start (landing) page
    def make_start_page(self):
        self.start = StartPage(self.container, self)

    # Function to execute when start button pressed
    def on_start_button_press(self):
        # is_valid_interface = (self.start.get_interface() != "")
        is_valid_project_setting = (self.start.get_project_settings() != "")

        # Valid user input
        if is_valid_project_setting:
            self.is_valid_project_setting = self.start.get_project_settings()

            # Wipe out current window
            self.container.destroy()

            # Add notebook to original
            self.make_main_page(self.pipe_spectrum_gui, self.pipe_recording_gui)

        else:  # invalid
            self.start.display_error_message()
            return

    def make_main_page(self, spectrum_pipe, recording_pipe):
        self.main_page = MainPage(self.parent, self, spectrum_pipe, recording_pipe,
                                  self.session)  # parent of main page is root

    def start_spectrum_process(self, center_freq, bandwidth):
        # Create sdr handler
        self.sdr_handler = CoverageHandler()
        self.sdr_handler.start(self.pipe_spectrum_process, center_freq, bandwidth)

    def stop_spectrum_process(self):
        self.sdr_handler.stop()

    def start_recording_process(self, center_freq, bandwidth):
        self.recording_handler = RecordingHandler()
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
            self.main_page.coverage_page.after(500, self.main_page.coverage_page.capture_canvas)

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

    # TODO: update with new coverage workflow
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
            self.main_page.coverage_page.disable_scan_button()

    # Save whatever plot is on the tkinter if valid heatmap
    def save_heatmap_plot(self, output_path, forceSave=False):

        if self.session.is_need_to_save() or forceSave:

            # Display only if dxf file opened and wifi scan done
            if self.dxf_opened and self.scan_done:
                self.main_page.coverage_page.save_heatmap_plot(output_path)

            elif not self.dxf_opened:
                self.main_page.coverage_page.coverage_info_panel.set_no_dxf_error_message()

            elif not self.scan_done:
                self.main_page.coverage_page.coverage_info_panel.set_no_wifi_scan_error_message()

            if not forceSave:
                self.session.set_no_need_to_save()

    # Generate and display created heatmap on tkinter canvas
    def display_heatmap(self):

        # If require to resave
        if self.session.is_need_to_save():

            # Rebuild heatmap first
            output_file_name = f"{self.session.get_dxf_prefix()}_{self.session.get_current_coverage_plot_num()}.png"
            saved_heatmap_path = f"{self.session.get_session_private_folder_path()}/{output_file_name}"
            self.save_heatmap_plot(saved_heatmap_path)
            self.session.increment_coverage_plot_num()

            # Set no need to save
            self.session.set_no_need_to_save()

        else:
            return

        # Display heatmap in tkinter canvas
        # don't display if no previous
        if self.session.get_prev_coverage_plot_num() > 0:
            self.image = tk.PhotoImage(file=saved_heatmap_path)

        else:
            self.image = tk.PhotoImage()

        self.main_page.coverage_page.coverage_canvas.create_image(
            0,
            0,
            image=self.image,
            anchor=tk.NW
        )

    def save_current_heatmap(self, dir):
        # Display only if dxf file opened and wifi scan done
        if self.dxf_opened and self.scan_done:
            output_file_name = f"{self.session.get_dxf_prefix()}_{self.session.get_current_coverage_save_num()}.png"
            output_file = f"{dir}/{output_file_name}"
            self.save_heatmap_plot(output_file, True)
            self.session.increment_coverage_save_num()
