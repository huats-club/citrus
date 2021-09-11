from scapy.config import conf
from scapy.interfaces import IFACES
from scapy.layers.dot11 import Dot11
from scapy.sendrecv import sniff


def packethandler(pkt):
    print(pkt)
    if pkt.haslayer(Dot11):
        print("hello")


conf.sniff_promisc = False
conf.use_pcap = True
print(IFACES.show())
mydev = IFACES.dev_from_index(8)
sniff(iface=mydev, prn=packethandler, store=0)

# https://github.com/secdev/scapy/issues/2230
# https://stackoverflow.com/questions/43314956/sniff-function-in-scapy-not-working-win
# https://www.geeksforgeeks.org/finding-all-wifi-devices-using-scapy-python/
# https://stackoverflow.com/questions/60309107/wireless-signal-strength-from-scapy-using-python3
# https://nmap.org/npcap/
