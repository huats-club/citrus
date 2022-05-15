from tabulate import tabulate


class SdrUtils:
    def __init__(self) -> None:
        pass

    @staticmethod
    def hovertext(sdr_entries):

        # Prepare tuple of (ssid, rssi)
        tuple_name_rssi = []
        for entry in sdr_entries:
            tuple_name_rssi.append((entry.name, entry.rssi))

        ret = []
        for (name, rssi) in tuple_name_rssi:
            ret.append([name, rssi])
        ret = sorted(ret, key=lambda x: x[0])

        return tabulate(ret, tablefmt="plain")
