import copy
import tkinter as tk
import tkinter.ttk as ttk

from model.WifiScanner import WifiScanner
from view.main.coverage_mode.sdr_mode.CoverageSdrTab import CoverageSdrTab
from view.main.coverage_mode.wifi_mode.CoverageWifiTab import CoverageWifiTab


class CoverageDataScanner(ttk.Frame):
    def __init__(self, parent, controller, coverage, *args, **kwargs):
        self.parent = parent
        self.controller = controller
        self.coverage = coverage

        # iid for entries
        self.idx = 0

        super().__init__(
            self.parent,
            # text="Data Scanner",
            *args, **kwargs
        )
        self.pack(
            side=tk.TOP,
            anchor=tk.NW,
            fill=tk.X
        )

        # Create main container
        self.container = ttk.Frame(self)
        self.container.pack(
            side=tk.TOP,
            anchor=tk.NW,
            fill=tk.BOTH
        )

        # create notebook to choose interface
        self.interfaces_selection = ttk.Notebook(
            self,
            style="primary.TNotebook",
            * args, **kwargs
        )
        self.interfaces_selection.pack(
            padx=10,
            pady=10,
            fill=tk.BOTH,
            expand=True  # ensures fill out the the parent
        )

        # Add SDR tab
        self.sdr_tab = CoverageSdrTab(
            self.interfaces_selection,
            self.controller
        )

        # Add Wifi tab
        self.wifi_tab = CoverageWifiTab(
            self.interfaces_selection,
            self.controller,
            self.coverage
        )

        self.interfaces_selection.add(
            self.wifi_tab,
            text="WIFI"
        )
        self.interfaces_selection.add(
            self.sdr_tab,
            text="SDR"
        )

        # Select wifi as main tab
        self.interfaces_selection.select(self.wifi_tab)

    def populate_wifi_scan_results(self, json_list):
        for json in json_list:
            ssid = json['ssid']
            bssid = json['bssid']
            freq = json['channel_frequency']
            channel = json['channel_number'] + "@" + json['channel_width']

            self.wifi_tab.display_all_panel.insert(
                parent="",
                index=self.idx,
                iid=self.idx,
                text="",
                values=(ssid, bssid, freq, channel)
            )
            self.idx += 1

    def clear_wifi_scan_results(self):
        self.wifi_tab.clear_all_wifi_panel()

    def get_wifi_data_tracked(self):
        # Get list of ssid tracked
        ssid_selected = self.wifi_tab.get_tracked_ssid_list()

        wifi_scanner = WifiScanner(filter=ssid_selected)
        wifi_list_json = wifi_scanner.scan()

        return copy.deepcopy(wifi_list_json)

    # Returns WIFI or SDR
    def get_current_tab_name(self):
        return self.interfaces_selection.tab(self.interfaces_selection.select(), 'text')
