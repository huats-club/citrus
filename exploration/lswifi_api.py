from lswifi import appsetup
from lswifi.client import Client, get_interface_info
from lswifi.wlanapi import WLAN

# core.list_interfaces(interfaces=WLAN.get_wireless_interfaces())
parser = appsetup.setup_parser()
args = parser.parse_args()
interfaces = WLAN.get_wireless_interfaces()
for interface in interfaces:
    print(get_interface_info(args, interface))
