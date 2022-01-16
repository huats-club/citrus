import random
import string

from tabulate import tabulate


class Point:
    def __init__(self, x, y, list_json):
        self.x = x
        self.y = y
        self.map = {}

        # Number of data sources from e.g. ssids in this point
        self.type_count = len(list_json)

        # preprocess the ssid and rssi into map of (ssid->rssi)
        for json in list_json:
            bssid = json['bssid']  # using mac address
            ssid = json['ssid']
            rssi = json['rssi']

            # print(f"{bssid} {ssid} {rssi}")

            # if bssid not in list(self.map.keys()):
            self.map[bssid] = (ssid, rssi)

    # Used to get string representation to display on tooltip
    def __str__(self):
        return self.to_table_string()

    def __repr__(self) -> str:
        s = "\n"
        return f"{self.x} {self.y} {self.__str__().replace(f'{s}', ' ')}"

    def to_table_string(self):
        # get list of ssid
        ssids = list(self.map.keys())

        # get list of rssi
        tuple_ssid_rssis = list(self.map.values())

        ret = []
        for (ssid, rssi) in tuple_ssid_rssis:
            ret.append([ssid, rssi])

        ret = sorted(ret, key=lambda x: x[0])

        return tabulate(ret, tablefmt="plain")

    def get_num_signal_sources(self):
        return self.type_count
