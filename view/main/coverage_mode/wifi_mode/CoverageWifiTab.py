import tkinter as tk
from tkinter import ttk


class CoverageWifiTab(ttk.Frame):
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

        # Currently selected row of data from list of all wifi
        self.current_selected_from_display_all = {}

        # Currently selected row of data from list of selected
        self.current_selected_from_display_selected = {}

        # String length for button
        self.STRING_LENGTH = 10

        # Create main container
        self.container = ttk.Frame(self)
        self.container.pack(
            padx=4,
            pady=4,
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

        # Create display treeview panel to show wifi ALL ssid scanned
        self.display_all_panel = ttk.Treeview(
            self.container,
            show='headings',
            style='primary.Treeview',
            columns=self.column_names,
            height=5
        )
        self.display_all_panel.pack(
            padx=4,
            pady=4,
            fill=tk.BOTH,
            expand=True,
            anchor=tk.NW,
            side=tk.TOP
        )

        # Setup columns and headings
        for column_name in self.column_names:
            self.display_all_panel.column(
                column_name,
                width=self.column_width[column_name],
                anchor=tk.W
            )
            self.display_all_panel.heading(
                column_name,
                text=column_name,
                anchor=tk.CENTER
            )

        # Create display treeview panel to show SELECTED SSID
        self.display_selected_panel = ttk.Treeview(
            self.container,
            show='headings',
            style='primary.Treeview',
            columns=self.column_names,
            height=5
        )
        self.display_selected_panel.pack(
            padx=4,
            pady=4,
            fill=tk.BOTH,
            expand=True,
            anchor=tk.NW,
            side=tk.BOTTOM
        )

        # Setup columns and headings
        for column_name in self.column_names:
            self.display_selected_panel.column(
                column_name,
                width=self.column_width[column_name],
                anchor=tk.W
            )
            self.display_selected_panel.heading(
                column_name,
                text=column_name,
                anchor=tk.CENTER
            )

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
            self.button_container,
            style="primary.Outline.TButton",
            text="Clear".center(self.STRING_LENGTH, ' ')
        )
        self.clear_button.pack(
            side=tk.RIGHT,
            padx=10,
            pady=(0, 10)
        )

        # Allow clicking of treeview items
        self.display_all_panel.bind('<ButtonRelease-1>', self.select_item_from_display_all)

        # Allow clicking of treeview items
        self.display_selected_panel.bind('<ButtonRelease-1>', self.select_item_from_display_selected)

    def select_item_from_display_all(self, a):
        curItem = self.display_all_panel.focus()
        data = self.display_all_panel.item(curItem)['values']

        idx = 0
        for name in self.column_names:
            self.current_selected_from_display_all[name] = data[idx]
            idx += 1

        print(self.current_selected_from_display_all)

    def select_item_from_display_selected(self, a):
        curItem = self.display_selected_panel.focus()
        data = self.display_selected_panel.item(curItem)['values']

        if len(data) == 0:
            return

        idx = 0
        for name in self.column_names:
            self.current_selected_from_display_selected[name] = data[idx]
            idx += 1

        print(self.current_selected_from_display_selected)
