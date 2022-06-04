from lswifi import appsetup
from lswifi.client import Client
from lswifi.wlanapi import WLAN

from model.wifi_entry import WifiEntry


class WifiScanner:
    def __init__(self, filter=[]):
        self.parser = appsetup.setup_parser()
        self.args = self.parser.parse_args()
        self.entries = []

        # filter of list of ssid to return
        self.filter = filter
        self.hasFilter = not (filter == [])

    def scan(self):
        self.entries = []

        try:

            # get all interfaces
            try:
                self.interfaces = WLAN.get_wireless_interfaces()
            except ValueError:
                print("Can't find wireless interfaces from WLAN")
                return

            # for all interface, scan for wlan
            for interface in self.interfaces:
                client = Client(self.args, interface)
                WLAN.scan(client.iface.guid)
                print(f"interface: {interface}")

                # process bss list
                wireless_network_bss_list = WLAN.get_wireless_network_bss_list(interface=interface)
                print(f"wireless_network_bss_list: {wireless_network_bss_list}")

                for bss in wireless_network_bss_list:
                    entry = self.pack_wifi_entry(bss)
                    print(f"entry: {entry}")

                    # append to json list only if bssid matches
                    if self.hasFilter:
                        if entry.bssid in self.filter:
                            self.entries += [entry]

                    else:
                        self.entries += [entry]

        except Exception as e:
            print(e)
            return

        # If not all detected, drop also
        if len(self.entries) != len(self.filter) and self.hasFilter == True:
            return []

        return self.entries

    def pack_wifi_entry(self, bss):
        bssid = str(bss.bssid).strip()
        channel_freq = str(bss.channel_frequency).strip()
        channel_num = str(bss.channel_number).strip()
        channel_width = str(bss.channel_width).strip()
        rssi = str(bss.rssi)
        ssid = str(bss.ssid).strip()
        entry = WifiEntry(ssid, bssid, rssi, channel_freq, channel_num, channel_width)
        return entry
