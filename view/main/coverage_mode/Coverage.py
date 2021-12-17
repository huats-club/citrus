import tkinter as tk
from tkinter import ttk

from app_parameters import app_parameters
from model.dxf2tk import dxf2tk
from model.WifiHeatmapPlotter import WifiHeatmapPlotter
from view.main.coverage_mode.CoverageBar import CoverageBar
from view.main.coverage_mode.CoverageCanvas import CoverageCanvas
from view.main.coverage_mode.CoverageDataScanner import CoverageDataScanner
from view.main.coverage_mode.CoverageFileMenu import CoverageFileMenu
from view.main.coverage_mode.CoverageInfoPanel import CoverageInfoPanel
from view.main.coverage_mode.CoverageValuesMenu import CoverageValuesMenu


class CoveragePage(ttk.Frame):
    def __init__(self, parent, controller, session, *args, **kwargs):
        self.parent = parent
        self.controller = controller
        self.session = session

        self.save_dir_path = self.session.get_session_workspace_path()

        # Save current canvas x and y bounds
        self.x_bound = -1
        self.y_bound = -1

        # Collect point (x,y) data
        self.recorded_points = []
        self.has_points = False

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
        self.coverage_file_menu = CoverageFileMenu(self.right_container, self.controller)

        # Create coverage value menu for rssi filtering
        self.coverage_value_menu = CoverageValuesMenu(self.right_container, self.controller)

        # Create coverage menu bar for right top container
        self.coverage_display_data = CoverageDataScanner(self.right_container, self.controller)

        # Create error message bar
        self.coverage_info_panel = CoverageInfoPanel(self.right_container, self.controller)

    def display_dxf(self, dxf):
        # Clear all recorded points if not already empty
        self.recorded_points = []

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

    def capture_canvas(self):
        self.coverage_canvas.capture()

    def set_no_dxf_error_message(self):
        self.coverage_info_panel.set_no_dxf_error_message()

    def set_load_dxf_error_message(self):
        self.coverage_info_panel.set_load_dxf_error_message()

    def disable_scan_button(self):
        self.coverage_display_data.disable_scan_button()  # TODO: change later

    def enable_scan_button(self):
        self.coverage_display_data.enable_scan_button()  # TODO: change later

    def populate_wifi_scan_results(self, json_list):
        self.coverage_display_data.populate_wifi_scan_results(json_list)  # TODO: change later

    def clear_wifi_scan_results(self):
        self.recorded_points = []
        self.has_points = False
        self.coverage_display_data.clear_wifi_scan_results()  # TODO: change later

    def enable_canvas_click(self):
        self.coverage_canvas.enable_click()

    def disable_canvas_click(self):
        self.coverage_canvas.disable_click()

    def add_point_data(self, x, y):
        # Get currently select wifi data
        wifi_selected = self.coverage_display_data.get_current_selected()  # TODO: change later

        # Prepared dictionary
        data = {
            app_parameters.POINT_KEY_TK_X: x,
            app_parameters.POINT_KEY_TK_Y: y,
            app_parameters.POINT_KEY_WIFI_DATA: wifi_selected
        }

        # Add to list
        self.recorded_points.append(
            data
        )

        # Indicate flag that points exist
        self.has_points = True

        # Save coordinates in log
        with open(self.controller.log_name, 'a+') as f:
            conv_x = data[app_parameters.POINT_KEY_TK_X]
            conv_y = data[app_parameters.POINT_KEY_TK_Y]
            f.write(f"x: {conv_x} | y: {conv_y}\n")

        # Save wifi data in json log
        with open(self.controller.log_json, 'a+') as f:
            f.write(f"{wifi_selected}\n")

    # Save whatever plot is on the tkinter if valid heatmap
    def save_heatmap_plot(self, output_path):

        # Save plot if points available
        if self.has_points:
            wifi_heatmap_plotter = WifiHeatmapPlotter(
                self.recorded_points, self.controller.get_floorplan_image_path())

            wifi_heatmap_plotter.save(output_path)

        # No points from wifi scan
        else:
            self.coverage_info_panel.set_no_wifi_scan_error_message()

    # Provide interface for save pane to call common function
    def update_save_path(self, path):
        self.save_dir_path = path

    # Provide interface for save pane to call common function
    def handle_save(self):
        self.controller.save_current_heatmap(self.save_dir_path)
