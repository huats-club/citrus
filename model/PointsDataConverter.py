import copy


# takes in a dictionary (x,y)->point and process to WifiHeatmapPlotter ready data
class PointsDataConverter:
    def __init__(self, points) -> None:

        # setup map of lists
        self.all_heatmap_survey_points = {}

        # shared x,y list for all possible heatmaps
        x_list = []
        y_list = []

        # map for store list of rssis
        heatmap_ssid_maps = {}

        for point in points.values():
            x = point.x
            y = point.y

            # append x and y to lists
            x_list.append(x)
            y_list.append(y)

            for bssid, (ssid, rssi) in point.map.items():

                if bssid not in heatmap_ssid_maps.keys():
                    heatmap_ssid_maps[bssid] = [int(rssi)]

                else:
                    heatmap_ssid_maps[bssid].append(int(rssi))

        # process all x,y to integer
        x_list = [int(n) for n in x_list]
        y_list = [int(n) for n in y_list]

        # populate to overall map
        for bssid, _ in heatmap_ssid_maps.items():
            self.all_heatmap_survey_points[bssid] = {
                'x': copy.deepcopy(x_list),
                'y': copy.deepcopy(y_list),
                'rssi': copy.deepcopy(heatmap_ssid_maps[bssid])
            }

    def process(self):
        return self.all_heatmap_survey_points
