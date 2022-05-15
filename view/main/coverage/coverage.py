import tkinter as tk
from re import S
from tkinter import ttk

from model.dxf2tk import dxf2tk
from view.main.coverage.coverage_bar import CoverageBar
from view.main.coverage.coverage_canvas import CoverageCanvas
from view.main.coverage.coverage_data_scanner import CoverageDataScanner
from view.main.coverage.coverage_file_menu import CoverageFileMenu
from view.main.coverage.coverage_info_panel import CoverageInfoPanel
from view.main.coverage.sdr_tab.sdr_tab import CoverageSdrTab


class CoveragePage(ttk.Frame):
    def __init__(self, parent, controller, *args, **kwargs):
        self.parent = parent
        self.controller = controller

        # Save current canvas x and y bounds
        self.x_bound = -1
        self.y_bound = -1

        super().__init__(self.parent,  *args, **kwargs)
        self.pack(
            padx=10,
            pady=10,
            fill=tk.BOTH,
            expand=True  # ensures fill out the the parent
        )

        # Create main container
        self.container = ttk.Frame(self)
        self.container.pack(
            padx=4,
            pady=4,
            fill=tk.BOTH,
            expand=True
        )

        # Create top half of container
        self.left_container = ttk.Frame(self.container)
        self.left_container.pack(
            padx=4,
            pady=4,
            fill=tk.BOTH,
            expand=True,
            side=tk.LEFT
        )

        # Create (menu) bottom half of container
        self.right_container = tk.Frame(self.container)
        self.right_container.pack(
            padx=4,
            pady=4,
            side=tk.RIGHT,
            fill=tk.BOTH
        )

        # Create canvas for left top container
        self.coverage_canvas = CoverageCanvas(self.left_container, self.controller, self)

        # Create bottom bar
        self.coverage_bar = CoverageBar(self.left_container, self.controller, self)

        # Create coverage menu to upload file
        self.coverage_file_menu = CoverageFileMenu(self.right_container, self.controller, self)

        # Create coverage menu bar for right top container
        self.coverage_display_data = CoverageDataScanner(self.right_container, self.controller, self)

        # Create error message bar
        self.coverage_info_panel = CoverageInfoPanel(self.right_container, self.controller)

    # Method is invoked to set the path of the directory to save plot images
    # NOTE: this result set to the pane might be changed by user input
    def set_coverage_save_path(self, path):
        self.coverage_bar.set_save_path(path)

    def set_floorplan_filepath_display(self, path):
        self.coverage_file_menu.set_dxf_filepath(path)

    # Draw on canvas given the dxf opened file
    def draw_dxf(self, dxf):

        # Create converter
        dxf2tk_converter = dxf2tk(self)

        # try to parse and make sense of dxf
        msp = dxf.modelspace()
        for e in msp:
            if e.dxftype() == 'LINE':
                dxf2tk_converter.add_line(e.dxf.start[0],
                                          e.dxf.start[1],
                                          e.dxf.end[0],
                                          e.dxf.end[1]
                                          )

            if e.dxftype() == 'ARC':
                dxf2tk_converter.add_arc(e.dxf.center[0],
                                         e.dxf.center[1],
                                         e.dxf.radius,
                                         e.dxf.start_angle,
                                         e.dxf.end_angle
                                         )

        converted_lines, converted_arcs = dxf2tk_converter.convert()

        for line in converted_lines:
            self.coverage_canvas.draw_line(
                line["start_x"],
                line["start_y"],
                line["end_x"],
                line["end_y"]
            )

        for arc in converted_arcs:
            self.coverage_canvas.draw_arc(
                arc["x_left_upper"],
                arc["y_left_upper"],
                arc["x_right_lower"],
                arc["y_right_lower"],
                arc["start_angle"],
                arc["extent"]
            )

    # Required method to get the driver value input
    def get_driver_input(self):
        return self.coverage_display_data.get_driver_input()

    def set_load_dxf_error_message(self):
        self.coverage_info_panel.set_load_dxf_error_message()

    def enable_canvas_click(self):
        self.coverage_canvas.enable_click()

    def disable_canvas_click(self):
        self.coverage_canvas.disable_click()

    # Clear canvas of all drawing
    def clear_canvas(self):
        self.coverage_canvas.delete("all")

    # Add point to (x, y) of canvas with attached hovertext when hover ontop point
    def add_point(self, x, y, hovertext):
        self.coverage_canvas.canvas_put_point(x, y, hovertext)

    # Checks which tab is currently tracked, e.g. "WIFI" or "SDR"
    def get_current_signal_tab(self):
        return self.coverage_display_data.get_current_tab_name()

    # Method is invoked by controller to update the list of scanned wifi ssids/bssids
    def populate_scanned_wifi_list(self, entries):
        self.coverage_display_data.populate_scanned_wifi_list(entries)

    # Method is invoked by controller to clear coverage in wifi mode
    def on_coverage_wifi_clear(self):
        self.coverage_display_data.coverage_wifi_clear()

    # Method is invoked by controller to get tracked bssid list in Wifi mode
    def get_wifi_tracked_bssid_list(self):
        return self.coverage_display_data.get_wifi_tracked_bssid_list()

    # Method is invoked by controller to set the heatmap allowed to be viewed after generated
    def set_name_heatmap_path_mapping(self, mapping):
        # populate ssid name to option menu
        self.coverage_bar.set_heatmap_selection(list(mapping.keys()))

    # Put up image to canvas, given path to image
    def put_image(self, path, points, hovertexts):
        # get path of ssid
        self.image = tk.PhotoImage(file=path)

        self.coverage_canvas.create_image(
            -30,
            -30,
            image=self.image,
            anchor=tk.NW
        )

        for idx in range(len(points)):
            point = points[idx]
            self.coverage_canvas.canvas_put_point(point[0], point[1], hovertexts[idx])

    def get_save_path(self):
        return self.coverage_bar.get_save_path()

    # Method is invoked to save path
    def save_plot(self, path=""):
        if path == "":
            return
        self.coverage_canvas.save_plot(path)

    def get_sdr_tab(self):
        return self.coverage_display_data.sdr_tab

    # Required method to disable calibration mode
    def disable_calibration(self):
        self.coverage_display_data.disable_calibration()

    # Required method to enable calibration mode
    def enable_calibration(self):
        self.coverage_display_data.enable_calibration()

    # Required method to set calibration in progress error
    def set_valid_calibration_message(self):
        self.coverage_display_data.display_calibration_message()

    # Required method to set calibration completed
    def set_calibration_complete_message(self):
        self.coverage_display_data.display_calibration_done()

    # Required method to set the error message that frequency not entered when calibration is done
    def set_invalid_calibration_message(self):
        self.enable_calibration()
        self.coverage_display_data.display_calibration_error_message()
