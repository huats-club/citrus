from scapy.config import conf
from scapy.interfaces import IFACES
from scapy.layers.dot11 import Dot11
from scapy.layers.inet6 import IPv6
from scapy.sendrecv import sniff

IFACE_NAME = "Realtek 8821AE Wireless LAN 802.11ac PCI-E NIC"
devices = set()


def packethandler(pkt):
    # if pkt.haslayer(Dot11):
    #     dot11_layer = pkt.getlayer(Dot11)
    #     if dot11_layer.addr2 and (dot11_layer.addr2 not in devices):
    #         devices.add(dot11_layer.addr2)
    #         print(dot11_layer.addr2)

    # print(pkt.summary())
    # print(pkt.show())
    # print(pkt.layers())
    if pkt.haslayer(IPv6):
        print("scapy.layers.inet6.IPv6")


conf.sniff_promisc = False
conf.use_pcap = True
print(IFACES.show())
# mydev = IFACES.dev_from_index(10)
sniff(iface=IFACE_NAME, prn=packethandler, store=0)

# https://github.com/secdev/scapy/issues/2230
# https://stackoverflow.com/questions/43314956/sniff-function-in-scapy-not-working-win
# https://www.geeksforgeeks.org/finding-all-wifi-devices-using-scapy-python/
# https://stackoverflow.com/questions/60309107/wireless-signal-strength-from-scapy-using-python3
# https://nmap.org/npcap/
