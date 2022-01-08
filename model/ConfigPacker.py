import copy

from config_parameters import config_parameters


class ConfigParser:
    def __init__(self):
        pass

    def pack_coverage_config(
            self, workspace_path, private_path, map_ssid_heatmap_path,
            recorded_points, current_tab, tab_tracked_data):

        base = {}

        # Pack workspace and private paths
        base[config_parameters.KEY_COVERAGE_WORKSPACE] = workspace_path
        base[config_parameters.KEY_COVERAGE_PRIVATE_WORKSPACE] = private_path

        # Pack ssid->heatmap path
        base[config_parameters.KEY_COVERAGE_PRIVATE_HEATMAPS] = copy.deepcopy(map_ssid_heatmap_path)

        # Pack current tab name
        base[config_parameters.KEY_COVERAGE_COVERAGE_CURRENT_TAB] = current_tab

        # Pack tracked item (dependent on current tab name)
        base[config_parameters.KEY_COVERAGE_CURRENT_TRACKED_DATA] = copy.deepcopy(tab_tracked_data)

        # Pack recorded points data
        packed_recorded_points = []

        for _, point in recorded_points.items():
            temp = {}

            # Pack coordinates
            temp[config_parameters.KEY_COVERAGE_RECORDED_POINTS_X] = point.x
            temp[config_parameters.KEY_COVERAGE_RECORDED_POINTS_Y] = point.y

            # Pack all ssid and rssi
            data = {}
            for ssid, rssi in point.map.items():
                data[ssid] = rssi
            temp[config_parameters.KEY_COVERAGE_RECORDED_POINTS_DATA] = copy.deepcopy(data)

            packed_recorded_points.append(copy.deepcopy(temp))

        base[config_parameters.KEY_COVERAGE_RECORDED_POINTS] = copy.deepcopy(packed_recorded_points)

        return base

    def parse_coverage_config(self, data):

        workspace_path = data[config_parameters.KEY_COVERAGE_WORKSPACE]
        private_path = data[config_parameters.KEY_COVERAGE_PRIVATE_WORKSPACE]

        map_ssid_heatmap_path = data[config_parameters.KEY_COVERAGE_PRIVATE_HEATMAPS]

        recorded_points = data[config_parameters.KEY_COVERAGE_RECORDED_POINTS]

        current_tab = data[config_parameters.KEY_COVERAGE_COVERAGE_CURRENT_TAB]

        tab_tracked_data = data[config_parameters.KEY_COVERAGE_CURRENT_TRACKED_DATA]

        return workspace_path, private_path, map_ssid_heatmap_path, recorded_points, current_tab, tab_tracked_data

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
