import copy

from config_parameters import config_parameters


class ConfigPacker:
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
