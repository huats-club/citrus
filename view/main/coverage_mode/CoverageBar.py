import tkinter as tk
from tkinter import ttk


class CoverageBar(ttk.Frame):
    def __init__(self, parent, controller, * args, **kwargs):
        self.parent = parent
        self.controller = controller

        super().__init__(
            self.parent,
            *args, **kwargs
        )
        self.pack(
            padx=5,
            pady=5,
            side=tk.BOTTOM,
            fill=tk.X
        )

        # String length for button
        self.STRING_LENGTH = 10

        # Container for view utilties
        self.view_container = ttk.Frame(self)
        self.view_container.pack(
            padx=5,
            pady=5,
            side=tk.LEFT,
            anchor=tk.NW
        )

        # Container for plot utilities
        self.plot_container = ttk.Frame(self)
        self.plot_container.pack(
            padx=5,
            pady=5,
            side=tk.RIGHT,
            anchor=tk.NE
        )

        # Create pan button
        self.pan_button = ttk.Button(
            self.view_container,
            style="primary.Outline.TButton",
            text="Pan".center(self.STRING_LENGTH, ' ')
        )
        self.pan_button.pack(
            side=tk.LEFT,
            padx=10,
            pady=5
        )

        # Create scan button
        self.scan_button = ttk.Button(
            self.view_container,
            style="primary.Outline.TButton",
            text="Scan".center(self.STRING_LENGTH, ' '),
            command=self.controller.do_scan
        )
        self.scan_button.pack(
            side=tk.LEFT,
            padx=10,
            pady=5
        )

        # Create plot button
        self.plot_button = ttk.Button(
            self.plot_container,
            style="primary.Outline.TButton",
            text="Plot".center(self.STRING_LENGTH, ' ')
        )
        self.plot_button.pack(
            side=tk.LEFT,
            padx=10,
            pady=5
        )

        # Create combine button
        self.combine_button = ttk.Button(
            self.plot_container,
            style="primary.Outline.TButton",
            text="Combine".center(self.STRING_LENGTH, ' ')
        )
        self.combine_button.pack(
            side=tk.RIGHT,
            padx=10,
            pady=5
        )

    def disable_scan_button(self):
        self.scan_button.state = tk.DISABLED

    def enable_scan_button(self):
        self.scan_button.state = tk.NORMAL
