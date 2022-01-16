import copy

from config_parameters import config_parameters


class ConfigParser:
    def __init__(self):
        pass

    def process_mac_addr(self, string):
        return string.replace(':', '#').replace(" ", "_").replace("(*)", "")

    def reconstruct_mac_addr(self, string):
        return string.replace('#', ':')

    def pack_coverage_config(
            self, workspace_path, private_path, floorplan_image_path, map_ssid_heatmap_path,
            recorded_points, current_tab, tab_tracked_data):

        base = {}

        # Pack workspace and private paths
        base[config_parameters.KEY_COVERAGE_WORKSPACE] = workspace_path
        base[config_parameters.KEY_COVERAGE_PRIVATE_WORKSPACE] = private_path
        base[config_parameters.KEY_COVERAGE_FLOORPLAN_IMAGE] = floorplan_image_path

        # Pack ssid->heatmap path
        temp = {}
        for name, path in map_ssid_heatmap_path.items():
            # fix: replace : in mac address to use in key without interfering with yaml
            temp[self.process_mac_addr(name)] = path
        base[config_parameters.KEY_COVERAGE_PRIVATE_HEATMAPS] = temp

        # Pack current tab name
        base[config_parameters.KEY_COVERAGE_COVERAGE_CURRENT_TAB] = current_tab

        # Pack tracked item (dependent on current tab name)
        temp_tracked_data = []
        for data in tab_tracked_data:
            temp_tracked_data.append(
                {
                    "bssid": data["bssid"],
                    "channel_frequency": int(data["channel_frequency"]),
                    "channel_number": int(data["channel_number"]),
                    "channel_width": int(data["channel_width"]),
                    "rssi": int(data["rssi"]),
                    "ssid": data["ssid"]
                }
            )
            temp_tracked_data
        base[config_parameters.KEY_COVERAGE_CURRENT_TRACKED_DATA] = temp_tracked_data

        # Pack recorded points data
        packed_recorded_points = []

        for _, point in recorded_points.items():
            temp = {}

            # Pack coordinates
            temp[config_parameters.KEY_COVERAGE_RECORDED_POINTS_X] = int(point.x)
            temp[config_parameters.KEY_COVERAGE_RECORDED_POINTS_Y] = int(point.y)

            # Pack all ssid and rssi
            data = {}
            for bssid, (ssid, rssi) in point.map.items():
                data[self.process_mac_addr(bssid)] = {"ssid": ssid, "rssi": int(rssi)}
            temp[config_parameters.KEY_COVERAGE_RECORDED_POINTS_DATA] = copy.deepcopy(data)
            packed_recorded_points.append(copy.deepcopy(temp))

        base[config_parameters.KEY_COVERAGE_RECORDED_POINTS] = copy.deepcopy(packed_recorded_points)

        return base

    def parse_coverage_config(self, data):

        workspace_path = data[config_parameters.KEY_COVERAGE_WORKSPACE]
        private_path = data[config_parameters.KEY_COVERAGE_PRIVATE_WORKSPACE]

        temp = data[config_parameters.KEY_COVERAGE_PRIVATE_HEATMAPS]
        map_ssid_heatmap_path = {}
        # process all the names to original mac addr form
        for name, path in temp.items():
            map_ssid_heatmap_path[self.reconstruct_mac_addr(name)] = path

        recorded_points = data[config_parameters.KEY_COVERAGE_RECORDED_POINTS]
        print(recorded_points)

        current_tab = data[config_parameters.KEY_COVERAGE_COVERAGE_CURRENT_TAB]

        tab_tracked_data = data[config_parameters.KEY_COVERAGE_CURRENT_TRACKED_DATA]

        floorplan_image = data[config_parameters.KEY_COVERAGE_FLOORPLAN_IMAGE]

        return workspace_path, private_path, floorplan_image, map_ssid_heatmap_path, recorded_points, current_tab, tab_tracked_data

    def pack_spectrum_config(self, start_freq, center_freq, end_freq, driver):

        base = {}

        base[config_parameters.KEY_SPECTRUM_DRIVER] = driver
        base[config_parameters.KEY_SPECTRUM_START_FREQ] = float(start_freq)
        base[config_parameters.KEY_SPECTRUM_CENTER_FREQ] = float(center_freq / 1e6)
        base[config_parameters.KEY_SPECTRUM_END_FREQ] = float(end_freq)

        return base

    def parse_spectrum_config(self, data):
        start_freq = data[config_parameters.KEY_SPECTRUM_START_FREQ]
        center_freq = data[config_parameters.KEY_SPECTRUM_CENTER_FREQ]
        end_freq = data[config_parameters.KEY_SPECTRUM_END_FREQ]
        driver = data[config_parameters.KEY_SPECTRUM_DRIVER]
        return str(start_freq), str(center_freq), str(end_freq), driver

    def pack_recording_config(self, start_freq, center_freq, end_freq, driver):

        base = {}

        base[config_parameters.KEY_RECORDING_DRIVER] = driver
        base[config_parameters.KEY_RECORDING_START_FREQ] = float(start_freq)
        base[config_parameters.KEY_RECORDING_CENTER_FREQ] = float(center_freq / 1e6)
        base[config_parameters.KEY_RECORDING_END_FREQ] = float(end_freq)

        return base

    def parse_recording_config(self, data):
        start_freq = data[config_parameters.KEY_RECORDING_START_FREQ]
        center_freq = data[config_parameters.KEY_RECORDING_CENTER_FREQ]
        end_freq = data[config_parameters.KEY_RECORDING_END_FREQ]
        driver = data[config_parameters.KEY_RECORDING_DRIVER]
        return str(start_freq), str(center_freq), str(end_freq), driver
