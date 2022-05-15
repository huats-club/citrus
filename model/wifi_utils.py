from tabulate import tabulate


class WifiUtils:
    def __init__(self) -> None:
        pass

    @staticmethod
    def hovertext(wifi_entries):

        # Prepare tuple of (ssid, rssi)
        tuple_ssid_rssis = []
        for entry in wifi_entries:
            tuple_ssid_rssis.append((entry.ssid, entry.rssi))

        ret = []
        for (ssid, rssi) in tuple_ssid_rssis:
            ret.append([ssid, rssi])
        ret = sorted(ret, key=lambda x: x[0])

        return tabulate(ret, tablefmt="plain")
