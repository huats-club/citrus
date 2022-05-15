class WifiEntry:
    def __init__(self, ssid, bssid, rssi, channel_frequency, channel_number, channel_width):
        self.ssid = ssid
        self.bssid = bssid
        self.rssi = rssi
        self.channel_frequency = channel_frequency
        self.channel_number = channel_number
        self.channel_width = channel_width

    def __str__(self) -> str:
        return f"{self.ssid} {self.bssid} {self.rssi} {self.channel_frequency}MHz {self.channel_number}@{self.channel_width}"

    def __repr__(self) -> str:
        return f"{self.ssid} {self.bssid} {self.rssi} {self.channel_frequency}MHz {self.channel_number}@{self.channel_width}"

    def values(self):
        return (self.ssid, self.bssid, self.channel_frequency, f"{self.channel_number}@{self.channel_width}")

    def format(self):
        pass
