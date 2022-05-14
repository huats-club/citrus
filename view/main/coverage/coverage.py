
import tkinter as tk
from tkinter import ttk

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
