from scapy.config import conf
from scapy.interfaces import IFACES
from scapy.layers.dot11 import Dot11Elt
from scapy.sendrecv import sniff

IFACE_NAME = "Realtek 8821AE Wireless LAN 802.11ac PCI-E NIC"
ap = []
packets = []


def PacketFilter(pkt):
    print(pkt.info)
    if pkt.haslayer(Dot11Elt) and pkt.type == 0 and pkt.subtype == 8:
        if pkt.addr2 not in ap:
            ap.append(pkt.addr2)


if __name__ == "__main__":
    conf.sniff_promisc = False
    conf.use_pcap = True
    print(IFACES.show())
    sniff(iface=IFACE_NAME, prn=PacketFilter, store=0, timeout=10)
    print(ap)
