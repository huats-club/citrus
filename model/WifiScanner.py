from lswifi import appsetup
from lswifi.client import Client
from lswifi.wlanapi import WLAN


class WifiScanner:
    def __init__(self, filter=[]):
        self.parser = appsetup.setup_parser()
        self.args = self.parser.parse_args()
        self.json_list = []

        # filter of list of ssid to return
        self.filter = filter
        self.hasFilter = not (filter == [])

    def scan(self):

        # get all interfaces
        self.interfaces = WLAN.get_wireless_interfaces()

        # for all interface, scan for wlan
        for interface in self.interfaces:
            client = Client(self.args, interface)
            WLAN.scan(client.iface.guid)

            # process bss list
            wireless_network_bss_list = client.get_bss_list(interface=interface)
            for bss in wireless_network_bss_list:
                json = self.bss2json(bss, self.args)

                # append to json list only if bssid matches
                if self.hasFilter:
                    if json['bssid'] in self.filter:
                        self.json_list += [json]

                else:
                    self.json_list += [json]

        return self.json_list

    def bss2json(self, bss, args):
        bssid_list = []

        # for bss in wireless_network_bss_list:
        # this is a list to check for dup bssids (may be expected for some APs which share same BSSID on 2.4 and 5 GHz radios - Cisco for example)
        bssid_list.append(str(bss.bssid))

        connected = False
        if bss.bssid.connected:
            connected = True
            if not args.json:
                bss.bssid.value += "(*)"

        json = {
            # "amendments": sorted(bss.amendments.elements),
            # "apname": str(bss.apname).strip(),
            "bssid": str(bss.bssid).strip(),
            # "bss_type=": str(bss.bss_type).strip(),
            "channel_frequency": str(bss.channel_frequency).strip(),
            "channel_number": str(bss.channel_number).strip(),
            "channel_width": str(bss.channel_width).strip(),
            # "connected": connected,
            # "ies": sorted(bss.ie_numbers.elements),
            # "ies_extension": sorted(bss.exie_numbers.elements),
            # "modes": sorted(bss.modes.elements),
            # "phy_type": str(bss.phy_type).strip(),
            # "rates_basic": [x for x in bss.wlanrateset.basic.split(" ")],
            # "rates_data": [x for x in bss.wlanrateset.data.split(" ")],
            "rssi": str(bss.rssi),
            # "security": str(bss.security).strip(),
            # "spatial_streams": str(bss.spatial_streams),
            "ssid": str(bss.ssid).strip()
            # "stations": str(bss.stations),
            # "uptime": str(bss.uptime).strip(),
            # "utilization": str(bss.utilization).strip(),
        }

        return json
