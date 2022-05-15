import config.app_parameters as app_parameters
import matplotlib
import matplotlib.cm as cm
import matplotlib.pyplot as plot
import numpy as np
from pylab import imread
from scipy.interpolate import Rbf


class WifiHeatmapPlotter:

    # Takes in pre-processed data points to save and plot
    def __init__(self, survey_points, floorplan_image_path):
        self.survey_points = survey_points
        self.floorplan_image_path = floorplan_image_path

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
            self.survey_points[app_parameters.HEATMAP_PLOT_X].append(x)
            self.survey_points[app_parameters.HEATMAP_PLOT_Y].append(y)
            for k in self.survey_points.keys():
                if k in ['x', 'y', 'ssid']:
                    continue
                self.survey_points[k] = [0 if x is None else x for x in self.survey_points[k]]
                self.survey_points[k].append(min(self.survey_points[k]))

        # Do plot scaling
        self.num_x = int(self.floorplan_width/4)
        self.num_y = int(self.num_x/(self.floorplan_width/self.floorplan_height))
        x = np.linspace(0, self.floorplan_width, self.num_x)
        y = np.linspace(0, self.floorplan_height, self.num_y)
        gx, gy = np.meshgrid(x, y)
        self.gx, self.gy = gx.flatten(), gy.flatten()

        # Set plot figure size
        self.dpi = 300
        plot.rcParams['figure.dpi'] = (
            self.dpi
        )
        plot.rcParams['figure.figsize'] = (
            app_parameters.CANVAS_WIDTH / self.dpi,
            app_parameters.CANVAS_HEIGHT / self.dpi
        )
        self.fig, self.ax = plot.subplots(1)
        plot.margins(0, 0)
        plot.subplots_adjust(
            top=1,
            bottom=0,
            right=1,
            left=0,
            hspace=0,
            wspace=0
        )
        for item in [self.fig, self.ax]:
            item.patch.set_visible(False)

        # Fix plot threshold max and min
        self.vmin = min(self.survey_points[app_parameters.HEATMAP_PLOT_SIGNAL])
        self.vmax = max(self.survey_points[app_parameters.HEATMAP_PLOT_SIGNAL])

        if self.vmin != self.vmax:
            self.rbf = Rbf(
                self.survey_points[app_parameters.HEATMAP_PLOT_X],
                self.survey_points[app_parameters.HEATMAP_PLOT_Y],
                self.survey_points[app_parameters.HEATMAP_PLOT_SIGNAL],
                function='linear'
            )
            z = self.rbf(gx, gy)
            self.z = z.reshape((self.num_y, self.num_x))
        else:
            # Uniform array with the same color everywhere
            # (avoids interpolation artifacts)
            self.z = np.ones((self.num_y, self.num_x))*self.vmin

        # Render the interpolated data to the plot
        self.ax.axis('off')

        # Create color map for plot reference
        self.cmap = plot.get_cmap("RdYlGn")

        # begin color mapping
        self.norm = matplotlib.colors.Normalize(
            vmin=self.vmin,
            vmax=self.vmax,
            clip=True
        )
        self.mapper = cm.ScalarMappable(
            norm=self.norm,
            cmap=self.cmap
        )
        # end color mapping

    def save(self, output_path):

        self.image = self.ax.imshow(
            self.z,
            extent=(0, self.floorplan_width, self.floorplan_height, 0),
            alpha=0.5,
            zorder=100,
            cmap=self.cmap,
            vmin=self.vmin,
            vmax=self.vmax
        )

        # Draw floorplan itself to the lowest layer with full opacity
        self.ax.imshow(
            self.floorplan,
            interpolation='bicubic',
            zorder=1,
            alpha=1
        )

        # Show points
        for idx in range(0, len(self.survey_points[app_parameters.HEATMAP_PLOT_X])):
            if(self.survey_points[app_parameters.HEATMAP_PLOT_X][idx], self.survey_points[app_parameters.HEATMAP_PLOT_Y][idx]) in self.floorplan_corner_coord:
                continue

            self.ax.plot(
                self.survey_points[app_parameters.HEATMAP_PLOT_X][idx],
                self.survey_points[app_parameters.HEATMAP_PLOT_Y][idx],
                zorder=200,
                marker='o',
                # markeredgecolor='black',
                markeredgewidth=0.4,
                markersize=2.5,
                markerfacecolor=self.mapper.to_rgba(self.survey_points[app_parameters.HEATMAP_PLOT_SIGNAL][idx])
            )

        # Save plot
        plot.savefig(
            output_path,
            dpi=self.dpi,
            bbox_inches='tight'
        )
        plot.close('all')
