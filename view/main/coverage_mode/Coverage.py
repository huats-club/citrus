import tkinter as tk
from tkinter import ttk

from model.dxf2tk import dxf2tk
from model.tk2dxf import tk2dxf
from view.main.coverage_mode.CoverageBar import CoverageBar
from view.main.coverage_mode.CoverageCanvas import CoverageCanvas
from view.main.coverage_mode.CoverageDataDisplay import CoverageDataDisplay
from view.main.coverage_mode.CoverageFileMenu import CoverageFileMenu
from view.main.coverage_mode.CoverageInfoPanel import CoverageInfoPanel
from view.main.coverage_mode.CoverageValuesMenu import CoverageValuesMenu


class CoveragePage(ttk.Frame):
    def __init__(self, parent, controller, *args, **kwargs):
        self.parent = parent
        self.controller = controller

        # Save current canvas x and y bounds
        self.x_bound = -1
        self.y_bound = -1

        # Collect point (x,y) data
        self.recorded_points = []

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
        self.coverage_bar = CoverageBar(self.left_container, self.controller)

        # Create coverage menu to upload file
        self.coverage_file_menu = CoverageFileMenu(self.right_container, self.controller)

        # Create coverage menu bar for right top container
        self.coverage_display_data = CoverageDataDisplay(self.right_container, self.controller)

        # Create coverage value menu for right top container
        self.coverage_value_menu = CoverageValuesMenu(self.right_container, self.controller)

        # Create error message bar
        self.coverage_info_panel = CoverageInfoPanel(self.right_container, self.controller)

    def display_dxf(self, dxf):
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

    def set_no_dxf_error_message(self):
        self.coverage_info_panel.warning_text.set("Error! No dxf file selected.")
        self.after(5000, self.clear_no_dxf_error_message)

    def clear_no_dxf_error_message(self):
        self.coverage_info_panel.warning_text.set("")

    def disable_scan_button(self):
        self.coverage_display_data.disable_scan_button()

    def enable_scan_button(self):
        self.coverage_display_data.enable_scan_button()

    def populate_wifi_scan_results(self, json_list):
        self.coverage_display_data.populate_wifi_scan_results(json_list)

    def clear_wifi_scan_results(self):
        self.coverage_display_data.clear_wifi_scan_results()

    def enable_canvas_click(self):
        self.coverage_canvas.enable_click()

    def disable_canvas_click(self):
        self.coverage_canvas.disable_click()

    def add_point_data(self, x, y):
        # Get currently select wifi data
        wifi_selected = self.coverage_display_data.get_current_selected()

        # Prepared dictionary
        data = {
            'tk_x': x,
            'tk_y': y,
            'wifi_data_selected': wifi_selected
        }

        # Add to list
        self.recorded_points.append(
            data
        )

        tk2dxf_converter = tk2dxf(self)

        # Save coordinates in log
        with open(self.controller.log_name, 'a+') as f:
            conv_x = tk2dxf_converter.tk2dxf_convert_x(data['tk_x'])
            conv_y = tk2dxf_converter.tk2dxf_convert_y(data['tk_y'])
            f.write(f"x: {conv_x} | y: {conv_y}\n")

        # Save wifi data in json log
        with open(self.controller.log_json, 'a+') as f:
            f.write(f"{wifi_selected}\n")
