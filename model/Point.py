import random
import string


class Point:
    def __init__(self, x, y, list_wifi_json):
        self.x = x
        self.y = y
        self.map = {}

        # preprocess the ssid and rssi into map of (ssid->rssi)
        for json in list_wifi_json:
            ssid = json['ssid']
            rssi = json['rssi']

            if ssid not in self.map:
                self.map[ssid] = rssi

            # for now, generate a random string to append
            # if ssid exists
            else:
                rand = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(2))
                self.map[ssid+rand] = rssi
