import tkinter as tk
from tkinter import ttk


class CoverageMenu(ttk.LabelFrame):
    def __init__(self, parent, controller, *args, **kwargs):
        self.parent = parent
        self.controller = controller

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
            fill=tk.BOTH
        )

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
            'channel'
        ]

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
                width=100,
                anchor=tk.CENTER
            )
            self.panel.heading(
                column_name,
                text=column_name,
                anchor=tk.CENTER
            )

    def populate_wifi_scan_results(self, json_list):
        idx = 0
        for json in json_list:

            ssid = json['ssid']
            bssid = json['bssid']
            rssi = json['rssi']
            channel = json['channel_frequency'] + json['channel_number'] + json['channel_width']

            self.panel.insert(
                parent="",
                index=idx,
                iid=idx,
                text="",
                values=(ssid, bssid, rssi, channel)
            )
            idx += 1
