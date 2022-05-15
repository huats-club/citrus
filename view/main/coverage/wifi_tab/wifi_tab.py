import tkinter as tk
from tkinter import ttk

from model.wifi_entry import WifiEntry


class CoverageWifiTab(ttk.Frame):
    def __init__(self, parent, controller, coverage, *args, **kwargs):
        self.parent = parent
        self.controller = controller
        self.coverage = coverage

        super().__init__(
            self.parent,
            *args, **kwargs
        )
        self.pack(
            side=tk.BOTTOM,
            fill=tk.X
        )

        # String length for button
        self.STRING_LENGTH = 10

        # uuid for selected
        self.iid = 0

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

        # Create main container
        self.container = ttk.Frame(self)
        self.container.pack(
            padx=4,
            pady=4,
            side=tk.TOP,
            anchor=tk.NW,
            fill=tk.BOTH
        )

        # Label to inform display ALL ssid scanned
        self.display_all_panel_label = ttk.Label(
            self.container,
            text="All SSID available:"
        )
        self.display_all_panel_label.pack(
            side=tk.TOP,
            anchor=tk.NW,
            padx=10,
            pady=5
        )

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

        # Label to inform display ALL ssid scanned
        self.display_tracked_panel_label = ttk.Label(
            self.container,
            text="SSID tracked:"
        )
        self.display_tracked_panel_label.pack(
            side=tk.TOP,
            anchor=tk.NW,
            padx=10,
            pady=5
        )

        # Create display treeview panel to show SELECTED SSID
        self.display_tracked_panel = ttk.Treeview(
            self.container,
            show='headings',
            style='primary.Treeview',
            columns=self.column_names,
            height=5
        )
        self.display_tracked_panel.pack(
            padx=4,
            pady=4,
            fill=tk.BOTH,
            expand=True,
            anchor=tk.NW,
            side=tk.BOTTOM
        )

        # Setup columns and headings
        for column_name in self.column_names:
            self.display_tracked_panel.column(
                column_name,
                width=self.column_width[column_name]
            )
            self.display_tracked_panel.heading(
                column_name,
                text=column_name,
                anchor=tk.CENTER
            )

        # Container for button utilities
        self.button_container = ttk.Frame(self)
        self.button_container.pack(
            padx=5,
            side=tk.TOP,
            anchor=tk.CENTER
        )

        # Create scan button
        self.scan_button = ttk.Button(
            self.button_container,
            style="primary.TButton",
            text="Scan".center(self.STRING_LENGTH, ' '),
            command=lambda: self.controller.on_coverage_wifi_scan(self.coverage)
        )
        self.scan_button.pack(
            side=tk.LEFT,
            padx=10,
            pady=(0, 10)
        )

        # Create clear button
        self.clear_button = ttk.Button(
            self.button_container,
            style="secondary.TButton",
            text="Clear".center(self.STRING_LENGTH, ' '),
            command=lambda: self.controller.on_coverage_wifi_clear(self.coverage)
        )
        self.clear_button.pack(
            side=tk.LEFT,
            padx=10,
            pady=(0, 10)
        )

        # Create down button
        self.track_button = ttk.Button(
            self.button_container,
            style="success.TButton",
            text="Track".center(self.STRING_LENGTH, ' '),
            command=lambda: self.move_item_to_selected()
        )
        self.track_button.pack(
            side=tk.LEFT,
            padx=10,
            pady=(0, 10)
        )

        # Create down button
        self.untrack_button = ttk.Button(
            self.button_container,
            style="danger.TButton",
            text="Untrack".center(self.STRING_LENGTH, ' '),
            command=lambda: self.move_item_to_all()
        )
        self.untrack_button.pack(
            side=tk.RIGHT,
            padx=10,
            pady=(0, 10)
        )

        # Currently selected row of data from list of all wifi
        self.current_selected_from_display_all = None
        self.current_selected_iid_from_display_all = 0

        # Currently selected row of data from list of tracked wifi
        self.current_selected_from_display_tracked = None
        self.current_selected_iid_from_display_tracked = 0

        # Allow clicking of treeview items
        self.display_all_panel.bind('<ButtonRelease-1>', self.select_item_from_display_all)

        # Allow clicking of treeview items
        self.display_tracked_panel.bind('<ButtonRelease-1>', self.select_item_from_display_tracked)

    # Insert data to display all
    def insert_to_scanned_panel(self, ssid, bssid, channel_freq, channel_width, channel_num):
        # Prepare data
        channel = str(channel_num) + "@" + str(channel_width)

        data = (ssid, bssid, channel_freq, channel)

        self.display_all_panel.insert(
            parent='', index=self.iid, iid=self.iid,
            values=tuple(data)
        )
        self.iid += 1

    # Store clicked item in the ALL pane corresponding to click action
    def select_item_from_display_all(self, a):
        curItem = self.display_all_panel.focus()
        data = self.display_all_panel.item(curItem)['values']
        self.current_selected_iid_from_display_all = curItem

        temp = {}
        try:
            idx = 0
            for name in self.column_names:
                temp[name] = data[idx]
                idx += 1
        except IndexError:
            return

        self.current_selected_from_display_all = WifiEntry(temp["ssid"], temp["bssid"], "", temp["freq"], "", "")

    # Store clicked item from the tracked pane to click action
    def select_item_from_display_tracked(self, a):
        curItem = self.display_tracked_panel.focus()
        data = self.display_tracked_panel.item(curItem)['values']
        self.current_selected_iid_from_display_tracked = curItem

        temp = {}
        try:
            idx = 0
            for name in self.column_names:
                temp[name] = data[idx]
                idx += 1
        except IndexError:
            return

        self.current_selected_from_display_tracked = WifiEntry(
            temp["ssid"], temp["bssid"], "", temp["freq"], "", "")

    # Move the selected item in the Display ALL panel to selected panel
    def move_item_to_selected(self):
        self.display_tracked_panel.insert(
            parent='', index=self.iid, iid=self.iid,
            values=tuple(self.current_selected_from_display_all.values())
        )
        self.iid += 1

        # delete away from all tracked
        self.display_all_panel.delete(self.current_selected_iid_from_display_all)

    # Move the selected item from the Display tracked panel to all panel
    def move_item_to_all(self):
        self.display_all_panel.insert(
            parent='', index=self.iid, iid=self.iid,
            values=tuple(self.current_selected_from_display_tracked.values())
        )
        self.iid += 1

        # delete away from all tracked
        self.display_tracked_panel.delete(self.current_selected_iid_from_display_tracked)

    # Clear display all pane
    def clear_display_all_pane(self):
        self.display_all_panel.delete(*self.display_all_panel.get_children())
        self.current_selected_from_display_all = None
        self.current_selected_iid_from_display_all = 0

    # Clear display tracked pane
    def clear_display_tracked_pane(self):
        self.display_tracked_panel.delete(*self.display_tracked_panel.get_children())
        self.current_selected_from_display_tracked = None
        self.current_selected_iid_from_display_tracked = 0

    # Method is invoked by controller to get wifi bssid entry
    def get_wifi_tracked_bssid_list(self):
        bssid_list = []
        idx = 1
        for child in self.display_tracked_panel.get_children():
            all_data = self.display_tracked_panel.item(child)["values"]
            bssid_list.append(all_data[idx])  # assumes first item is bssid
        return bssid_list
