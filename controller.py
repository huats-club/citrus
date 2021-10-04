import datetime as datetime
import sys
import tkinter as tk
from multiprocessing import Pipe

import ezdxf

from app_parameters import app_parameters
from model.SDRHandler import SDRHandler
from model.Session import Session
from model.WifiScanner import WifiScanner
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

        # Reset dxf load variable
        self.dxf_opened = False

        # Scan results done
        self.scan_done = False

        # Current wifi log
        ts = datetime.datetime.date(datetime.datetime.now())
        self.log_name = fr"{app_parameters.WORKSPACE_FOLDER}/log_{ts}.txt"
        self.log_json = fr"{app_parameters.WORKSPACE_FOLDER}/{ts}.txt"

        # Create new session object
        self.session = Session()

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

        if self.dxf_opened == False:
            self.dxf_filepath, self.dxf_filename = self.main_page.coverage_page.coverage_file_menu.get_dxf_filepath_selected()

            # remove extensions from dxf filename
            self.dxf_filename = self.dxf_filename.replace(".dxf", "")

            # Save filename into session
            self.session.save_dxf_name(self.dxf_filename)

            try:
                dxf = ezdxf.readfile(self.dxf_filepath)

            except IOError:
                print(f'Not a DXF file or a generic I/O error.')
                sys.exit(1)
            except ezdxf.DXFStructureError:
                print(f'Invalid or corrupted DXF file.')
                sys.exit(2)

            # For debugging
            print(f"Opened {self.dxf_filepath}")

            # Save file as class member
            self.dxf = dxf

            # Display dxf file
            self.display_dxf()

            # Cache the image of display on tkinter canvas after display
            self.floorplan_saved_image_path = fr"{app_parameters.PRIVATE_FOLDER}\{self.dxf_filename}.png"
            self.main_page.coverage_page.after(500, self.main_page.coverage_page.capture_canvas)

            # Enable plotting of points
            self.main_page.coverage_page.enable_canvas_click()

        else:
            print("Dxf already opened, consider clearing canvas first")
            self.main_page.coverage_page.disable_canvas_click()

    def display_dxf(self):
        self.main_page.coverage_page.display_dxf(self.dxf)

        # Flag to indicate dxf already opened
        self.dxf_opened = True

    def clear_dxf_from_canvas(self):
        if self.dxf_opened == True:
            self.main_page.coverage_page.coverage_canvas.delete("all")
            self.dxf_opened = False

            self.main_page.coverage_page.clear_wifi_scan_results()

            # Disable canvas click
            self.main_page.coverage_page.disable_canvas_click()

        else:
            print("nothing to clear")

    def do_scan(self):

        # clear scan first
        self.main_page.coverage_page.clear_wifi_scan_results()

        # Do scan only if dxf is opened
        if self.dxf_opened:

            if self.scan_done:
                self.main_page.coverage_page.clear_wifi_scan_results()
                self.scan_done = False

            # If wifi, run lswifi scan
            if self.current_interface == app_parameters.INTERFACE_WIFI:
                wifi_scanner = WifiScanner()
                results = wifi_scanner.scan()
                self.main_page.coverage_page.populate_wifi_scan_results(results)

                # Indicate scan is done
                self.scan_done = True

            # If limesdr, run limesdr scan
            if self.current_interface == app_parameters.INTERFACE_SDR:
                print("scan sdr")

        # Else, prompt dxf to be loaded
        else:
            self.main_page.coverage_page.set_no_dxf_error_message()
            self.main_page.coverage_page.disable_scan_button()

    def configure_rssi_sensitivity(self):
        print("configure rssi sensitivity")

    # Save whatever plot is on the tkinter if valid heatmap
    def save_heatmap_plot(self):

        if self.session.is_need_to_save():

            # Display only if dxf file opened and wifi scan done
            if self.dxf_opened and self.scan_done:
                self.main_page.coverage_page.save_heatmap_plot()

            elif not self.dxf_opened:
                self.main_page.coverage_page.coverage_info_panel.set_no_dxf_error_message()

            elif not self.scan_done:
                self.main_page.coverage_page.coverage_info_panel.set_no_wifi_scan_error_message()

            self.session.set_no_need_to_save()

    # Display created heatmap on tkinter canvas
    def display_heatmap(self):

        # If require to resave
        if self.session.is_need_to_save():

            # Rebuild heatmap first
            self.save_heatmap_plot()

            # Set no need to save
            self.session.set_no_need_to_save()

        # Display heatmap in tkinter canvas
        self.image = tk.PhotoImage(
            file=f"{app_parameters.WORKSPACE_FOLDER}/{self.session.get_dxf_prefix()}_{self.session.get_prev_plot_num()}.png"
        )
        self.main_page.coverage_page.coverage_canvas.create_image(
            0,
            0,
            image=self.image,
            anchor=tk.NW
        )
