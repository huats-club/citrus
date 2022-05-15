# takes in a dictionary (x,y)->point
class SdrResultAggregator:
    def __init__(self, map_coord_sdr_entries) -> None:

        # x,y list for heatmaps
        self.x_list = []
        self.y_list = []

        # list of max rssi created
        self.aggregated_rssi = []

        for (x, y), entries in map_coord_sdr_entries.items():

            self.x_list.append(x)
            self.y_list.append(y)

            temp_max = -1000
            for entry in entries:
                if int(entry.rssi) > temp_max:
                    temp_max = int(entry.rssi)

            self.aggregated_rssi.append(temp_max)

    def process(self):
        return {'x': self.x_list, 'y': self.y_list, 'rssi': self.aggregated_rssi}
