import tkinter as tk
from tkinter import ttk

from config_parameters import config_parameters
from model.ConfigPacker import ConfigParser
from model.dxf2tk import dxf2tk
from model.Point import Point
from model.WifiHeatmapPlotter import WifiHeatmapPlotter
from view.main.coverage_mode.CoverageBar import CoverageBar
from view.main.coverage_mode.CoverageCanvas import CoverageCanvas
from view.main.coverage_mode.CoverageDataScanner import CoverageDataScanner
from view.main.coverage_mode.CoverageFileMenu import CoverageFileMenu
from view.main.coverage_mode.CoverageInfoPanel import CoverageInfoPanel


class CoveragePage(ttk.Frame):
    def __init__(self, parent, controller, session, *args, **kwargs):
        self.parent = parent
        self.controller = controller
        self.session = session

        # Get full resolved path to workspace
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
        self.coverage_display_data.populate_wifi_scan_results(json_list)

    def clear_wifi_scan_results(self):
        self.recorded_points = {}
        self.has_points = False
        self.coverage_display_data.clear_wifi_scan_results()

    def clear_sdr_scan_results(self):
        self.recorded_points = {}
        self.has_points = False
        self.coverage_display_data.clear_sdr_scan_results()

    def enable_canvas_click(self):
        self.coverage_canvas.enable_click()

    def disable_canvas_click(self):
        self.coverage_canvas.disable_click()

    def add_point_data(self, x, y):

        # create key to put inside maps
        key = (x, y)

        # get signal strength data of current mode tracked
        if self.coverage_display_data.get_current_tab_name() == "WIFI":
            wifi_list_json = self.coverage_display_data.get_wifi_data_tracked()
            print(wifi_list_json)

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

        # SDR
        else:
            # get dict (name->freq)
            sdr_name_freq_dict = self.coverage_display_data.get_sdr_data_tracked()
            print(sdr_name_freq_dict)

            # add freq and name to point
            point = Point(x, y, sdr_name_freq_dict)
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
            current_ssid_type = self.get_current_heatmap_name()
            output_file_name = f"{self.session.get_dxf_prefix()}_{current_ssid_type}_{self.session.get_current_coverage_save_num()}.png"
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
            -30,
            -30,
            image=self.image,
            anchor=tk.NW
        )

        self.coverage_canvas.canvas_put_point_again(self.recorded_points)

    def get_current_heatmap_name(self):
        return self.coverage_bar.get_current_heatmap_name()

    def setup_page_from_config(self, config_dict):
        workspace_path, private_path, map_ssid_heatmap_path, \
            recorded_points, current_tab, tab_tracked_data = ConfigParser().parse_coverage_config(config_dict)
        # print(f"paths: {workspace_path} {private_path}")
        # print(f"heatmaps created: {map_ssid_heatmap_path}")
        # print(f"recorded points: {recorded_points}")
        # print(f"current tab: {current_tab}")
        # print(f"tracked data: {tab_tracked_data}")

        # Save session workspace and private cached folder relative paths
        self.save_dir_path = workspace_path
        self.session.set_session_workspace_path(workspace_path)
        self.session.set_session_private_folder_path(private_path)

        # Plot points onto canvas
        self.recorded_points = {}
        for data in recorded_points:
            x = data[config_parameters.KEY_COVERAGE_RECORDED_POINTS_X]
            y = data[config_parameters.KEY_COVERAGE_RECORDED_POINTS_Y]
            map_data = data[config_parameters.KEY_COVERAGE_RECORDED_POINTS_DATA]
            list_json = []
            for ssid, rssi in map_data.items():
                list_json.append({"ssid": ssid, "rssi": rssi})
            self.recorded_points[(x, y)] = Point(x, y, list_json)
        self.has_points = True
        self.coverage_canvas.canvas_put_point_again(self.recorded_points)

        # Put image and populate ssid list to select to put onto canvas
        self.map_ssid_heatmap_path = map_ssid_heatmap_path
        if len(list(map_ssid_heatmap_path.keys())) > 0:
            self.coverage_bar.set_heatmap_selection(list(map_ssid_heatmap_path.keys()))
            self.put_image("Combined")  # Put combined image as head

        # Set tracked data into GUI
        if current_tab == "WIFI":

            # Set current tab
            self.coverage_display_data.set_current_interface(is_wifi=True)

            # Tab's tracked data is wifi scanned data
            for item in tab_tracked_data:
                self.coverage_display_data.wifi_tab.insert(item)

        else:
            # Set current tab
            self.coverage_display_data.set_current_interface(is_wifi=False)

            for x in tab_tracked_data:
                for name, freq in x.items():
                    self.coverage_display_data.sdr_tab.insert(name, freq)
