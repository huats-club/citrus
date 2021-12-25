import random
import string

from tabulate import tabulate


class Point:
    def __init__(self, x, y, list_wifi_json):
        self.x = x
        self.y = y
        self.map = {}

        # Number of data sources from e.g. ssids in this point
        self.type_count = len(list_wifi_json)

        # preprocess the ssid and rssi into map of (ssid->rssi)
        for json in list_wifi_json:
            ssid = json['ssid']
            rssi = json['rssi']

            if ssid not in self.map:
                self.map[ssid] = rssi

            # for now, generate a random string to append
            # if ssid exists
            else:
                rand = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(2))
                self.map[ssid+rand] = rssi

    # Used to get string representation to display on tooltip
    def __str__(self):
        return self.to_table_string()

    def __repr__(self) -> str:
        s = "\n"
        return f"{self.x} {self.y} {self.__str__().replace(f'{s}', ' ')}"
        return self.__str__()

    def to_table_string(self):
        # get list of ssid
        ssids = list(self.map.keys())

        # get list of rssi
        rssis = list(self.map.values())

        ret = []
        for idx in range(len(ssids)):
            ret.append([ssids[idx], rssis[idx]])

        ret = sorted(ret, key=lambda x: x[0])

        return tabulate(ret, tablefmt="plain")

    def get_num_signal_sources(self):
        return self.type_count
