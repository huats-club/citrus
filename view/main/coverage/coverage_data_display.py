import copy
import tkinter as tk
from tkinter import ttk


class CoverageDataDisplay(ttk.LabelFrame):
    def __init__(self, parent, controller, *args, **kwargs):
        self.parent = parent
        self.controller = controller

        # Currently selected row of data
        self.current_selected = {}

        # String length for button
        self.STRING_LENGTH = 10

        super().__init__(
            self.parent,
            text="AP Menu",
            *args, **kwargs
        )
        self.pack(
            padx=10,
            pady=10,
            side=tk.TOP,
            anchor=tk.NW,
            fill=tk.X
        )

        # iid for entries
        self.idx = 0

        # Create panel for display ssid, strength, mac and channel
        self.panel_container = ttk.Frame(self)
        self.panel_container.pack(
            padx=10,
            pady=(10, 5),
            side=tk.TOP,
            anchor=tk.NW,
            fill=tk.BOTH
        )

        # Create column name list
        self.column_names = [
            'ssid',
            'bssid',
            'rssi',
            'freq',
            'channel[#@MHz]'
        ]

        self.column_width = {
            'ssid': 160,
            'bssid': 140,
            'rssi': 40,
            'freq': 50,
            'channel[#@MHz]': 120
        }

        # Create display treeview panel to show wifi data
        self.panel = ttk.Treeview(
            self.panel_container,
            show='headings',
            style='primary.Treeview',
            columns=self.column_names
        )
        self.panel.pack(
            padx=4,
            pady=4,
            fill=tk.BOTH,
            expand=True,
            side=tk.LEFT
        )

        # Setup columns and headings
        for column_name in self.column_names:
            self.panel.column(
                column_name,
                width=self.column_width[column_name],
                anchor=tk.W
            )
            self.panel.heading(
                column_name,
                text=column_name,
                anchor=tk.CENTER
            )

        # # Allow clicking of treeview items
        # self.panel.bind('<ButtonRelease-1>', self.selectItem)

        # Container for button utilities
        self.button_container = ttk.Frame(self)
        self.button_container.pack(
            padx=5,
            side=tk.BOTTOM,
            anchor=tk.CENTER
        )

        # Create scan button
        self.scan_button = ttk.Button(
            self.button_container,
            style="primary.Outline.TButton",
            text="Scan".center(self.STRING_LENGTH, ' ')
        )
        self.scan_button.pack(
            side=tk.LEFT,
            padx=10,
            pady=(0, 10)
        )

        # Create clear button
        self.clear_button = ttk.Button(
            self.button_container,
            style="primary.Outline.TButton",
            text="Clear".center(self.STRING_LENGTH, ' ')
        )
        self.clear_button.pack(
            side=tk.RIGHT,
            padx=10,
            pady=(0, 10)
        )
