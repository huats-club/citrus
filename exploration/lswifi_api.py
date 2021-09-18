from lswifi import appsetup
from lswifi.client import Client, get_interface_info
from lswifi.core import parse_bss_list_and_print
from lswifi.wlanapi import WLAN

# core.list_interfaces(interfaces=WLAN.get_wireless_interfaces())
parser = appsetup.setup_parser()
args = parser.parse_args()
interfaces = WLAN.get_wireless_interfaces()
for interface in interfaces:
    # print(get_interface_info(args, interface))
    pass

client = Client(args, interface)
data = client.get_bss_list(interface=interface)
parse_bss_list_and_print(data, args)
