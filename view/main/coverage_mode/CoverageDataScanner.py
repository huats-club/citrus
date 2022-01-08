import copy
import math
import tkinter as tk
import tkinter.ttk as ttk

from model.CoverageHandler import CoverageSingleHandler
from model.WifiScanner import WifiScanner
from view.main.coverage_mode.sdr_mode.CoverageSdrTab import CoverageSdrTab
from view.main.coverage_mode.wifi_mode.CoverageWifiTab import CoverageWifiTab
from view.main.SelectDriverPane import SelectDriverPane


class CoverageDataScanner(ttk.Frame):
    def __init__(self, parent, controller, coverage, *args, **kwargs):
        self.parent = parent
        self.controller = controller
        self.coverage = coverage

        # iid for entries
        self.idx = 0

        # is first run
        self.is_first_scan = True
        self.sdr_handler = None

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

        # Create select driver
        self.select_driver_pane = SelectDriverPane(self, self.controller)

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

        # note when notebook tab change
        self.interfaces_selection.bind('<<NotebookTabChanged>>', self.switch_SDR_2_wifi_tab)

    def switch_SDR_2_wifi_tab(self, a):
        if self.get_current_tab_name() == "WIFI":
            self.is_first_scan = True

            if self.sdr_handler != None:
                self.sdr_handler.close()
                self.sdr_handler = None

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

        # clear sdr handler to prepare new
        if self.sdr_handler != None:
            self.sdr_handler.close()
            self.sdr_handler = None
            self.is_first_scan = True

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

    def get_sdr_data_tracked(self):

        # get dict of { (name, freq), ... } tracked
        tracked_freq_names = self.sdr_tab.get_tracked_list()

        # store names and freqs
        names = []
        freqs = []

        # calculate best range
        bandwidth = 13e6
        min_freq = 100e9
        max_freq = 0
        for pair in tracked_freq_names:
            name, freq = list(pair.items())[0]
            # print(f"current freq: {freq}")

            names.append(name)
            freqs.append(freq)

            if freq > max_freq:
                max_freq = freq

            if freq < min_freq:
                min_freq = freq

        # print(f"min freq: {min_freq}, max_freq: {max_freq}")
        scan_center_freq = (min_freq + max_freq) / 2

        # run sdr scan
        if self.is_first_scan:
            self.sdr_handler = CoverageSingleHandler()
            self.sdr_handler.start(scan_center_freq, bandwidth)
            dbm_data = self.sdr_handler.get_result()
            self.is_first_scan = False
        else:
            dbm_data = self.sdr_handler.get_result()

        # track if each has freq to be tracked
        # TODO: verify if tracked freqs are in this range
        scan_freq_inc = bandwidth / len(dbm_data)
        start_freq = scan_center_freq - 0.5*bandwidth
        end_freq = scan_center_freq + 0.5*bandwidth
        print(f"start freq: {start_freq}, center_freq: {scan_center_freq}, end_freq: {end_freq}")
        print(f"freq increment: {scan_freq_inc:.5f}")

        # pack into dict ("wifi": name, "rssi": dbm)
        ans = []
        for idx in range(len(freqs)):
            # compute idx to search
            located_center_idx = math.ceil((freqs[idx] - start_freq) / scan_freq_inc)
            left_bound_idx = located_center_idx - 3
            right_bound_idx = located_center_idx + 3

            # prevent out of bounds
            if left_bound_idx < 0:
                left_bound_idx = 0
            if right_bound_idx > len(dbm_data):
                right_bound_idx = len(dbm_data)

            # print(f"searching: {left_bound_idx} -> {right_bound_idx}")

            # find the max dbm
            max_dbm_found = -100
            for idx2 in range(left_bound_idx, right_bound_idx+1):
                if idx2 < len(dbm_data) and dbm_data[idx2] > max_dbm_found:
                    max_dbm_found = dbm_data[idx2]
                else:
                    max_dbm_found = -100
            # print(f"found max: {max_dbm_found:.5f}")

            temp = {}
            temp['ssid'] = names[idx]
            temp['rssi'] = max_dbm_found
            ans.append(temp)

        print(ans)
        return ans

    # Returns WIFI or SDR
    def get_current_tab_name(self):
        return self.interfaces_selection.tab(self.interfaces_selection.select(), 'text')

    def set_current_interface(self, is_wifi=True):
        if is_wifi:
            self.interfaces_selection.select(self.wifi_tab)
        else:
            self.interfaces_selection.select(self.sdr_tab)
