import copy


# takes in a dictionary (x,y)->point and process to WifiHeatmapPlotter ready data
class SdrResultsConverter:
    def __init__(self, map_coord_sdr_entries) -> None:
        # setup map of lists
        self.all_heatmap_survey_points = {}

        # shared x,y list for all possible heatmaps
        x_list = []
        y_list = []

        # map for store list of rssis
        heatmap_name_maps = {}

        for (x, y), entries in map_coord_sdr_entries.items():
            # append x and y to lists
            x_list.append(x)
            y_list.append(y)

            for entry in entries:
                if entry.name not in heatmap_name_maps.keys():
                    heatmap_name_maps[entry.name] = [int(entry.rssi)]

                else:
                    heatmap_name_maps[entry.name].append(int(entry.rssi))

        # process all x,y to integer
        x_list = [int(n) for n in x_list]
        y_list = [int(n) for n in y_list]

        # populate to overall map
        for name, _ in heatmap_name_maps.items():
            self.all_heatmap_survey_points[name] = {
                'x': copy.deepcopy(x_list),
                'y': copy.deepcopy(y_list),
                'rssi': copy.deepcopy(heatmap_name_maps[name])
            }

    def process(self):
        return self.all_heatmap_survey_points
