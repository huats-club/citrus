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
            padx=10,
            pady=10,
            side=tk.BOTTOM,
            anchor=tk.NW,
            fill=tk.BOTH
        )

        self.STRING_LENGTH = 10

        # Create container
        self.container = ttk.Frame(self)
        self.container.pack(
            side=tk.TOP,
            anchor=tk.NW,
            fill=tk.BOTH
        )

        # Create pan button
        self.pan_button = ttk.Button(
            self.container,
            style="primary.TButton",
            text="Pan".center(self.STRING_LENGTH, ' ')
        )
        self.pan_button.pack(
            side=tk.LEFT,
            padx=10,
            pady=(20, 0)
        )

        # Create scan button
        self.scan_button = ttk.Button(
            self.container,
            style="primary.TButton",
            text="Scan".center(self.STRING_LENGTH, ' ')
        )
        self.scan_button.pack(
            side=tk.LEFT,
            padx=10,
            pady=(20, 0)
        )

        # Create min value button
        self.min_button = ttk.Button(
            self.container,
            style="primary.TButton",
            text="Min".center(self.STRING_LENGTH, ' ')
        )
        self.min_button.pack(
            side=tk.LEFT,
            padx=10,
            pady=(20, 0)
        )

        # Create max value button
        self.max_button = ttk.Button(
            self.container,
            style="primary.TButton",
            text="Max".center(self.STRING_LENGTH, ' ')
        )
        self.max_button.pack(
            side=tk.LEFT,
            padx=10,
            pady=(20, 0)
        )

        # Create plot button
        self.plot_button = ttk.Button(
            self.container,
            style="primary.TButton",
            text="Plot".center(self.STRING_LENGTH, ' ')
        )
        self.plot_button.pack(
            side=tk.LEFT,
            padx=10,
            pady=(20, 0)
        )

        # Create combine button
        self.combine_button = ttk.Button(
            self.container,
            style="primary.TButton",
            text="Combine".center(self.STRING_LENGTH, ' ')
        )
        self.combine_button.pack(
            side=tk.RIGHT,
            padx=10,
            pady=(20, 0)
        )
