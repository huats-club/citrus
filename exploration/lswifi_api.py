from lswifi import core
from lswifi.wlanapi import WLAN

core.list_interfaces(interfaces=WLAN.get_wireless_interfaces())
