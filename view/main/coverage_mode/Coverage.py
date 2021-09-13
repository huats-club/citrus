import tkinter as tk
from tkinter import ttk

from view.main.coverage_mode.CoverageMenu import CoverageMenu


class CoveragePage(ttk.Frame):
    def __init__(self, parent, controller, *args, **kwargs):
        self.parent = parent
        self.controller = controller

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
            padx=10,
            pady=10,
            fill=tk.BOTH,
            expand=True
        )

        # Create top half of container
        self.top_container = ttk.Frame(self.container)
        self.top_container.pack(
            padx=10,
            pady=10,
            fill=tk.BOTH,
            expand=True,
            side=tk.TOP
        )

        # Create (menu) bottom half of container
        self.bottom_container = ttk.Frame(self.container)
        self.bottom_container.pack(
            padx=10,
            pady=10,
            fill=tk.BOTH,
            expand=True,
            side=tk.BOTTOM
        )

        # Create canvas for left top container

        # Create coverage menu bar for right top container
        self.coverage_menu = CoverageMenu(self.top_container)
