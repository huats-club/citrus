import copy
import random
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
            self.controller,
            self.coverage
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

    def clear_sdr_scan_results(self):
        self.sdr_tab.clear_all_sdr_panel()

    def get_wifi_data_tracked(self):
        # Get list of ssid tracked
        tracked_list_mac = self.wifi_tab.get_tracked_list()

        # If no ssid, return empty list
        if len(tracked_list_mac) == 0:
            return []

        wifi_scanner = WifiScanner(filter=tracked_list_mac)
        wifi_list_json = wifi_scanner.scan()

        # fill up with fake entry if bssid not found
        for bssid in tracked_list_mac:
            has_entry = False

            # check if exists at least 1 json entry for bssid
            for json in wifi_list_json:
                if bssid == json['bssid']:
                    has_entry = True
                    break

            if not has_entry:
                wifi_list_json.append({
                    "bssid": bssid,
                    "channel_frequency": 0,
                    "channel_number": 0,
                    "channel_width": 0,
                    "rssi": -100,
                    "ssid": self.wifi_tab.bssid2ssid(bssid)
                })

        return copy.deepcopy(wifi_list_json)

    # TODO: finish up the logic to conform to wifi data input
    def get_sdr_data_tracked(self):

        # get dict of { (name, freq), ... } tracked
        tracked_freq_names = self.sdr_tab.get_tracked_list()

        # run sdr scan

        # track if each has freq to be tracked

        # pack into dict ("wifi": name, "rssi": dbm)
        # MOCK DATA to run test interface
        ans = []
        for dic in tracked_freq_names:
            temp = {}
            temp['ssid'] = list(dic.keys())[0]
            temp['rssi'] = random.randrange(-50, -5)
            ans.append(temp)

        return ans

    # Returns WIFI or SDR
    def get_current_tab_name(self):
        return self.interfaces_selection.tab(self.interfaces_selection.select(), 'text')
