import tkinter as tk
from tkinter import ttk

from model.dxf2tk import dxf2tk
from model.Point import Point
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

        # Collect point (x,y) data in a dict/hashmap of (x,y) as key
        self.recorded_points = dict()
        self.has_points = False

        # Collect map of name of ssid's heatmap and path
        self.map_ssid_heatmap_path = {}

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

        # TODO: fix this later
        # Create coverage value menu for rssi filtering
        self.coverage_value_menu = CoverageValuesMenu(self.right_container, self.controller)

        # Create coverage menu bar for right top container
        self.coverage_display_data = CoverageDataScanner(self.right_container, self.controller, self)

        # Create error message bar
        self.coverage_info_panel = CoverageInfoPanel(self.right_container, self.controller)

    def display_dxf(self, dxf):
        # Clear all recorded points if not already empty
        self.recorded_points = {}

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

    def capture_canvas(self, path=""):
        self.coverage_canvas.capture(path)

    def set_no_dxf_error_message(self):
        self.coverage_info_panel.set_no_dxf_error_message()

    def set_load_dxf_error_message(self):
        self.coverage_info_panel.set_load_dxf_error_message()

    def populate_wifi_scan_results(self, json_list):
        self.coverage_display_data.populate_wifi_scan_results(json_list)  # TODO: change later

    def clear_wifi_scan_results(self):
        self.recorded_points = {}
        self.has_points = False
        self.coverage_display_data.clear_wifi_scan_results()  # TODO: change later

    def enable_canvas_click(self):
        self.coverage_canvas.enable_click()

    def disable_canvas_click(self):
        self.coverage_canvas.disable_click()

    # TODO: amend
    def add_point_data(self, x, y):

        # create key to put inside maps
        key = (x, y)

        # get signal strength data of current mode tracked
        if self.coverage_display_data.get_current_tab_name() == "WIFI":
            wifi_list_json = self.coverage_display_data.get_wifi_data_tracked()

            # if no wifi tracked, dont add point
            # TODO: add error message
            if len(wifi_list_json) == 0:
                return None

            # preprocess wifi data to Point
            point = Point(x, y, wifi_list_json)
            self.recorded_points[key] = point

            # Indicate flag that points exist
            self.has_points = True

            # return created point for recording
            return point

    # Provide interface for save pane to call common function
    def update_save_path(self, path):
        self.save_dir_path = path

    # Provide interface for save pane to call common function
    def handle_save(self):
        self.save_current_heatmap(self.save_dir_path)

    def save_heatmap_plot(self, output_path, data):

        # Save plot if points available
        if self.has_points:
            wifi_heatmap_plotter = WifiHeatmapPlotter(
                data, self.controller.get_floorplan_image_path())

            wifi_heatmap_plotter.save(output_path)

            return True

        # No points from wifi scan
        else:
            self.coverage_info_panel.set_no_wifi_scan_error_message()
            return False

    # Save by grabbing current screen
    def save_current_heatmap(self, dir):
        if self.controller.isValid():
            output_file_name = f"{self.session.get_dxf_prefix()}_{self.session.get_current_coverage_save_num()}.png"
            output_file = f"{dir}/{output_file_name}"
            self.capture_canvas(output_file)
            self.session.increment_coverage_save_num()

    def get_points(self):
        return self.recorded_points

    def set_ssid_heatmap_path(self, map):
        # save map
        self.map_ssid_heatmap_path = map

        # populate ssid name to option menu
        self.coverage_bar.set_heatmap_selection(list(map.keys()))

    # Put up image to canvas, given path to image
    def put_image(self, ssid):

        # plot nothing if nothing
        if ssid == "":
            return

        else:
            # get path of ssid
            path = self.map_ssid_heatmap_path[ssid]
            self.image = tk.PhotoImage(file=path)

        self.coverage_canvas.create_image(
            0,
            0,
            image=self.image,
            anchor=tk.NW
        )
