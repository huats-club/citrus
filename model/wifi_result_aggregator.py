# takes in a dictionary (x,y)->point
class WifiResultAggregator:
    def __init__(self, map_coord_wifi_entries) -> None:

        # x,y list for heatmaps
        self.x_list = []
        self.y_list = []

        # list of max rssi created
        self.aggregated_rssi = []

        for (x, y), entries in map_coord_wifi_entries.items():

            self.x_list.append(x)
            self.y_list.append(y)

            temp_max = -1000

            for entry in entries:
                print(f"now {entry}: { int(entry.rssi)}")
                if int(entry.rssi) > temp_max:
                    temp_max = int(entry.rssi)
                    print(f"temp max: {temp_max}")

            self.aggregated_rssi.append(temp_max)

    def process(self):
        print(f"self.aggregated_rssi: {self.aggregated_rssi}")
        return {'x': self.x_list, 'y': self.y_list, 'rssi': self.aggregated_rssi}
