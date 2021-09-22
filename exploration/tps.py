import json
import os
import time

from model.WifiScanner import WifiScanner


def collect_data(wifi_scanner, idx):
    # Do scan
    json_data = wifi_scanner.scan()

    # Dump to file name
    with open(f'exploration/wifi_data/data_{idx}.json', 'w') as f:
        json.dump(json_data, f)

    # Do delay
    time.sleep(10)


def collect_data_set():
    count = 1
    wifi_scanner = WifiScanner()

    # Collect point 1
    collect_data(wifi_scanner, count)
    count += 1

    # Collect point 2
    collect_data(wifi_scanner, count)
    count += 1

    # Collect point 3
    collect_data(wifi_scanner, count)
    count += 1


if __name__ == "__main__":

    # Check folder path for user data
    if not os.path.exists("exploration/wifi_data"):
        os.makedirs("exploration/wifi_data")

    # collect_data_set()
