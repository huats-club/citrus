import tkinter as tk
from tkinter import ttk

from model.dxf2tk import dxf2tk
from view.main.coverage.coverage_bar import CoverageBar
from view.main.coverage.coverage_canvas import CoverageCanvas
from view.main.coverage.coverage_data_scanner import CoverageDataScanner
from view.main.coverage.coverage_file_menu import CoverageFileMenu
from view.main.coverage.coverage_info_panel import CoverageInfoPanel


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

    def set_load_dxf_error_message(self):
        self.coverage_info_panel.set_load_dxf_error_message()

    def enable_canvas_click(self):
        self.coverage_canvas.enable_click()

    def disable_canvas_click(self):
        self.coverage_canvas.disable_click()

    def capture_canvas(self, path=""):
        self.coverage_canvas.capture(path)
