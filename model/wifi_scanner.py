# from lswifi import appsetup
# from lswifi.client import Client
# from lswifi.wlanapi import WLAN

import subprocess

from model.wifi_entry import WifiEntry


class WifiScanner:
    def __init__(self, filter=[]):
        # self.parser = appsetup.setup_parser()
        # self.args = self.parser.parse_args()
        self.entries = []

        # filter of list of ssid to return
        self.filter = filter
        self.hasFilter = not (filter == [])

        # # get all interfaces
        # try:
        #     self.interfaces = WLAN.get_wireless_interfaces()
        # except Exception as e:
        #     print(e)
        #     return

    def scan(self):
        self.entries = []

        # try:
        #     self.interfaces = WLAN.get_wireless_interfaces()

        #     # for all interface, scan for wlan
        #     for interface in self.interfaces:
        #         client = Client(self.args, interface)
        #         WLAN.scan(client.iface.guid)

        #         # process bss list
        #         wireless_network_bss_list = WLAN.get_wireless_network_bss_list(interface=interface)
        #         print(f"wireless_network_bss_list: {wireless_network_bss_list}")

        #         for bss in wireless_network_bss_list:
        #             entry = self.pack_wifi_entry(bss)
        #             # print(f"entry: {entry}")

        #             # append to json list only if bssid matches
        #             if self.hasFilter:
        #                 if entry.bssid in self.filter:
        #                     self.entries += [entry]

        #             else:
        #                 self.entries += [entry]

        # except Exception as e:
        #     print(e)
        #     print(f"self.entries: {self.entries}")

        #     return self.entries

        # # # If not all detected, drop also
        # # if len(self.entries) != len(self.filter) and self.hasFilter == True:
        # #     return []

        f = open('lswifi1.log', 'w')
        subprocess.run(["lswifi"], stdout=f)
        f.close()

        f = open('lswifi1.log', 'r')
        lines = f.readlines()
        f.close()

        i = 0
        for line in lines:
            if(line[0] == '-'):
                ind = i
            i = i+1

        for i in range(ind+1):
            lines.pop(0)

        final = []
        for line in lines:
            tmp = line.split()
            # print(tmp)
            for word in tmp:
                if(word.find(':') != -1 and len(word) > 15):
                    # print(word)
                    ind = (tmp.index(word))
            if(ind == 0):
                tmp.insert(0, 'FUB')
                # print(tmp)
            else:
                tmp.insert(0, " ".join(tmp[0:ind]))
                del tmp[1:ind+1]
                # print(tmp)
            final.append(tmp)

        # Process into format required
        for parsed in final:

            print(f"{parsed}")

            ssid = parsed[0]
            bssid = parsed[1].replace("(*)", "")
            rssi = parsed[2]
            freq = parsed[5]

            # print(f"parsed[4]: {parsed[4]}")
            temp = parsed[4].split("@")
            cnum = temp[0]
            cwidth = temp[1]

            entry = WifiEntry(ssid, bssid, rssi, freq, cnum, cwidth)

            if self.hasFilter:
                if entry.bssid in self.filter:
                    self.entries += [entry]

            else:
                self.entries += [entry]

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
