from collections import defaultdict

import matplotlib
import matplotlib.cm as cm
import matplotlib.pyplot as plot
import numpy as np
from app_parameters import app_parameters
from matplotlib.font_manager import FontManager
from pylab import imread
from scipy.interpolate import Rbf


class WifiHeatmapPlotter:
    def __init__(self, x_y_wifidata, floorplan_image_path, output_name):

        self.floorplan_image_path = floorplan_image_path
        self.output_name = output_name

        # Prepare data into plottable format
        self.survey_points = defaultdict(list)
        store = []
        for entry in x_y_wifidata:
            temp = {}

            for k, v in entry.items():
                if k == app_parameters.POINT_KEY_TK_X:
                    temp[app_parameters.WIFI_HEATMAP_PLOT_X] = int(v)

                elif k == app_parameters.POINT_KEY_TK_Y:
                    temp[app_parameters.WIFI_HEATMAP_PLOT_Y] = int(v)

                elif k == app_parameters.POINT_KEY_WIFI_DATA:
                    temp = {**temp, **v}

            store.append(temp)

        for item in store:
            for k, v in item.items():
                self.survey_points[k].append(item[k])

        # convert list of string to int
        self.survey_points[app_parameters.WIFI_HEATMAP_PLOT_X] = [
            int(x) for x in self.survey_points[app_parameters.WIFI_HEATMAP_PLOT_X]
        ]

        self.survey_points[app_parameters.WIFI_HEATMAP_PLOT_Y] = [
            int(x) for x in self.survey_points[app_parameters.WIFI_HEATMAP_PLOT_Y]
        ]

        self.survey_points['rssi'] = [
            int(x) for x in self.survey_points['rssi']
        ]

        print(self.survey_points)

        # Prepare for plot
        self.prepare_plot()

    def prepare_plot(self):
        # Read in floorplan image
        self.floorplan = imread(self.floorplan_image_path)
        self.floorplan_width = len(self.floorplan[0])
        self.floorplan_height = len(self.floorplan) - 1
        self.floorplan_corner_coord = [
            (0, 0), (0, self.floorplan_height),
            (self.floorplan_width, 0), (self.floorplan_width, self.floorplan_height)
        ]

        # Add in corner plot points
        for x, y in self.floorplan_corner_coord:
            self.survey_points['x'].append(x)
            self.survey_points['y'].append(y)
            for k in self.survey_points.keys():
                if k in ['x', 'y', 'ssid']:
                    continue
                self.survey_points['ssid'].append(None)
                self.survey_points[k] = [0 if x is None else x for x in self.survey_points[k]]
                self.survey_points[k].append(min(self.survey_points[k]))

        # Do plot scaling
        num_x = int(self.floorplan_width/4)
        num_y = int(num_x/(self.floorplan_width/self.floorplan_height))
        x = np.linspace(0, self.floorplan_width, num_x)
        y = np.linspace(0, self.floorplan_height, num_y)
        gx, gy = np.meshgrid(x, y)
        gx, gy = gx.flatten(), gy.flatten()

        # Set plot figure size
        # pp.rcParams['figure.figsize'] = (
        #     self.floorplan_width / 300, self.floorplan_height / 300
        # )
        fig, ax = plot.subplots(1)
        plot.margins(0, 0)
        plot.subplots_adjust(
            top=1,
            bottom=0,
            right=1,
            left=0,
            hspace=0,
            wspace=0
        )
        for item in [fig, ax]:
            item.patch.set_visible(False)
        # title = "rssi"
        # ax.set_title(title)

        # Fix plot threshold max and min
        vmin = min(self.survey_points['rssi'])
        vmax = max(self.survey_points['rssi'])

        if vmin != vmax:
            rbf = Rbf(
                self.survey_points['x'],
                self.survey_points['y'],
                self.survey_points['rssi'],
                function='linear'
            )
            z = rbf(gx, gy)
            z = z.reshape((num_y, num_x))
        else:
            # Uniform array with the same color everywhere
            # (avoids interpolation artifacts)
            z = np.ones((num_y, num_x))*vmin

        # Render the interpolated data to the plot
        ax.axis('off')

        # Create color map for plot reference
        cmap = plot.get_cmap("RdYlGn")

        # begin color mapping
        norm = matplotlib.colors.Normalize(
            vmin=vmin,
            vmax=vmax,
            clip=True
        )
        mapper = cm.ScalarMappable(
            norm=norm,
            cmap=cmap
        )
        # end color mapping

        image = ax.imshow(
            z,
            extent=(0, self.floorplan_width, self.floorplan_height, 0),
            alpha=0.5,
            zorder=100,
            cmap=cmap,
            vmin=vmin,
            vmax=vmax
        )

        # Draw floorplan itself to the lowest layer with full opacity
        ax.imshow(
            self.floorplan,
            interpolation='bicubic',
            zorder=1,
            alpha=1
        )
        # labelsize = FontManager.get_default_size() * 0.4

        # Show points
        for idx in range(0, len(self.survey_points['x'])):
            if(self.survey_points['x'][idx], self.survey_points['y'][idx]) in self.floorplan_corner_coord:
                continue

            ax.plot(
                self.survey_points['x'][idx],
                self.survey_points['y'][idx],
                zorder=200,
                marker='o',
                markeredgecolor='black',
                markeredgewidth=0.8,
                markersize=2.5,
                markerfacecolor=mapper.to_rgba(self.survey_points['rssi'][idx])
            )

        fname = fr"{app_parameters.WORKSPACE_FOLDER}\{self.output_name}.png"
        plot.savefig(
            fname,
            dpi=300,
            bbox_inches='tight'
        )
        plot.close('all')
