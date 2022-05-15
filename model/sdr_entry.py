class SdrEntry:
    def __init__(self, name, freq, rssi):
        self.name = name
        self.freq = freq
        self.rssi = rssi

    def __str__(self) -> str:
        return f"{self.name} {self.freq} {self.rssi}"

    def __repr__(self) -> str:
        return f"{self.name} {self.freq} {self.rssi}"

    def format(self):
        pass
