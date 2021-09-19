import asyncio

from lswifi import appsetup
from lswifi.client import Client
from lswifi.core import parse_bss_list_and_print
from lswifi.wlanapi import WLAN


def bsslist_2_json(wireless_network_bss_list, args):
    bssid_list = []
    json_out = []

    bss_len = len(wireless_network_bss_list)
    print(bss_len)

    for index, bss in enumerate(wireless_network_bss_list):
        # print(index, bss)
        pass
        # this is a list to check for dup bssids (may be expected for some APs which share same BSSID on 2.4 and 5 GHz radios - Cisco for example)
        bssid_list.append(str(bss.bssid))

        connected = False
        if bss.bssid.connected:
            connected = True
            if not args.json:
                bss.bssid.value += "(*)"

        json_out.append(
            {
                "amendments": sorted(bss.amendments.elements),
                "apname": str(bss.apname).strip(),
                "bssid": str(bss.bssid).strip(),
                "bss_type=": str(bss.bss_type).strip(),
                "channel_frequency": str(bss.channel_frequency).strip(),
                "channel_number": str(bss.channel_number).strip(),
                "channel_width": str(bss.channel_width).strip(),
                "connected": connected,
                "ies": sorted(bss.ie_numbers.elements),
                "ies_extension": sorted(bss.exie_numbers.elements),
                "modes": sorted(bss.modes.elements),
                "phy_type": str(bss.phy_type).strip(),
                "rates_basic": [x for x in bss.wlanrateset.basic.split(" ")],
                "rates_data": [x for x in bss.wlanrateset.data.split(" ")],
                "rssi": str(bss.rssi),
                "security": str(bss.security).strip(),
                "spatial_streams": str(bss.spatial_streams),
                "ssid": str(bss.ssid).strip(),
                "stations": str(bss.stations),
                "uptime": str(bss.uptime).strip(),
                "utilization": str(bss.utilization).strip(),
            }
        )

    print(json_out)


def main():

    # core.list_interfaces(interfaces=WLAN.get_wireless_interfaces())
    parser = appsetup.setup_parser()
    args = parser.parse_args()
    interfaces = WLAN.get_wireless_interfaces()
    for interface in interfaces:
        # print(get_interface_info(args, interface))
        pass

    client = Client(args, interface)
    WLAN.scan(client.iface.guid)  # replace async client.scan()
    data = client.get_bss_list(interface=interface)
    parse_bss_list_and_print(data, args)
    bsslist_2_json(data, args)


if __name__ == "__main__":
    main()
