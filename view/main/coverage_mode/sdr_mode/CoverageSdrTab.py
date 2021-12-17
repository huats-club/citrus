import tkinter as tk
from tkinter import ttk


class CoverageSdrTab(ttk.Frame):
    def __init__(self, parent, controller, *args, **kwargs):
        self.parent = parent
        self.controller = controller

        super().__init__(
            self.parent,
            *args, **kwargs
        )
        self.pack(
            side=tk.BOTTOM,
            fill=tk.X
        )

        # Create main container
        self.container = ttk.Frame(self)
        self.container.pack(
            padx=10,
            pady=10,
            side=tk.TOP,
            anchor=tk.NW,
            fill=tk.BOTH
        )

        # Create column name list to select active wifi
        self.column_names = [
            'ssid',
            'bssid',
            'freq',
            'channel[#@MHz]'
        ]

        self.column_width = {
            'ssid': 160,
            'bssid': 140,
            'freq': 50,
            'channel[#@MHz]': 120
        }

        # Create display treeview panel to show wifi ssid data
        self.panel = ttk.Treeview(
            self.container,
            show='headings',
            style='primary.Treeview',
            columns=self.column_names
        )
        self.panel.pack(
            padx=4,
            pady=4,
            fill=tk.BOTH,
            expand=True,
            anchor=tk.NW,
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
