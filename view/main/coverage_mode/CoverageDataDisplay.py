import tkinter as tk
from tkinter import ttk


class CoverageDataDisplay(ttk.LabelFrame):
    def __init__(self, parent, controller, *args, **kwargs):
        self.parent = parent
        self.controller = controller

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

        # Container for button utilities
        self.plot_container = ttk.Frame(self)
        self.plot_container.pack(
            padx=5,
            side=tk.BOTTOM,
            anchor=tk.CENTER
        )

        # Create scan button
        self.scan_button = ttk.Button(
            self.plot_container,
            style="primary.Outline.TButton",
            text="Scan".center(self.STRING_LENGTH, ' '),
            command=self.controller.do_scan
        )
        self.scan_button.pack(
            side=tk.LEFT,
            padx=10,
            pady=(0, 10)
        )

        # Create clear button
        self.clear_button = ttk.Button(
            self.plot_container,
            style="primary.Outline.TButton",
            text="Clear".center(self.STRING_LENGTH, ' '),
            command=self.clear_wifi_scan_results
        )
        self.clear_button.pack(
            side=tk.RIGHT,
            padx=10,
            pady=(0, 10)
        )

    def populate_wifi_scan_results(self, json_list):

        for json in json_list:
            ssid = json['ssid']
            bssid = json['bssid']
            rssi = json['rssi']
            freq = json['channel_frequency']
            channel = json['channel_number'] + "@" + json['channel_width']

            self.panel.insert(
                parent="",
                index=self.idx,
                iid=self.idx,
                text="",
                values=(ssid, bssid, rssi, freq, channel)
            )
            self.idx += 1

    def clear_wifi_scan_results(self):
        self.panel.delete(*self.panel.get_children())

    def disable_scan_button(self):
        self.scan_button.state = tk.DISABLED

    def enable_scan_button(self):
        self.scan_button.state = tk.NORMAL
