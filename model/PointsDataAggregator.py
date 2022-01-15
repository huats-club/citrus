# takes in a dictionary (x,y)->point
class PointDataAggregator:
    def __init__(self, points) -> None:

        # x,y list for heatmaps
        self.x_list = []
        self.y_list = []

        # list of max rssi created
        self.aggregated_rssi = []

        # temp map of point

        for point in points.values():
            x = point.x
            y = point.y

            self.x_list.append(x)
            self.y_list.append(y)

            map = point.map
            temp_max = -1000
            for bssid, (ssid, rssi) in map.items():
                if int(rssi) > temp_max:
                    temp_max = int(rssi)

            self.aggregated_rssi.append(temp_max)

    def process(self):
        return {'x': self.x_list, 'y': self.y_list, 'rssi': self.aggregated_rssi}
