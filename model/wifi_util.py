from model.wifi_scanner import WifiScanner


def process_wifi(tracked_list_mac, pipe):
    wifi_scanner = WifiScanner(filter=tracked_list_mac)
    pipe.send(wifi_scanner.scan())
