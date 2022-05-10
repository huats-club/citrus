import math
import tkinter as tk
from tkinter import ttk

import config.app_parameters as app_parameters
import matplotlib.backends.backend_tkagg as tkmatplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm


class RecordingWaterfallPlot(ttk.Frame):
    def __init__(self, parent, controller, recording, center_freq=740.3e6, bandwidth=20e6, *args, **kwargs):
        self.parent = parent
        self.controller = controller
        self.recording = recording

        super().__init__(self.parent, *args, **kwargs)
        self.pack(
            padx=5,
            pady=5,
            side=tk.TOP,
            fill=tk.BOTH,
            expand=True  # ensures that the panel file out the the parent
        )

        # generate (initial) timestamp marker
        # FIX: more points, nearer the peaks, to form a continuous bar
        ts_np = np.arange(500)

        # generate frequency bins
        freq_increment = bandwidth / 2048
        freq_bins = []
        start_freq = center_freq - bandwidth/2
        end_freq = center_freq + bandwidth/2
        while start_freq < end_freq:
            freq_bins.append(start_freq)
            start_freq += freq_increment
        freq_bins_np = np.asarray(freq_bins)

        # prepare 2d x,y data
        self.freq_bins_np_X, self.ts_np_Y = np.meshgrid(freq_bins_np, ts_np)

        # prepare z signal data store
        self.signal_np = np.zeros((0, 2048))

        # flag to indicate first data
        self.isFirst = True

        self.is_2d = False

    def set_2d(self):
        self.ax.azim = -90
        self.ax.elev = -90
        self.ax.dist = 6
        self.ax.set_box_aspect([3, 1, 1])
        self.is_2d = True

    def create_empty_3d_plot(self):
        # https://towardsdatascience.com/cyberpunk-style-with-matplotlib-f47404c9d4c5

        plt.style.use("seaborn-dark")

        for param in ['figure.facecolor', 'axes.facecolor', 'savefig.facecolor']:
            plt.rcParams[param] = '#212946'  # bluish dark grey

        for param in ['text.color', 'axes.labelcolor', 'xtick.color', 'ytick.color']:
            plt.rcParams[param] = '0.9'  # very light grey

        self.colors = [
            '#08F7FE',  # teal/cyan
            '#FE53BB',  # pink
            '#F5D300',  # yellow
            '#00ff41',  # matrix green
        ]

        self.fig = plt.figure(dpi=100)
        self.ax = self.fig.add_subplot(projection='3d')

        # set axis label
        self.ax.set_xlabel(app_parameters.WATERFALL_PLOT_LEGEND_X)
        self.ax.set_ylabel(app_parameters.WATERFALL_PLOT_LEGEND_Y)
        self.ax.set_zlabel(app_parameters.WATERFALL_PLOT_LEGEND_Z)

        # Change later to line plot+ with mock data
        self.canvas = tkmatplotlib.FigureCanvasTkAgg(
            self.fig,
            self
        )
        self.canvas.get_tk_widget().pack(
            side=tk.TOP,
            fill=tk.BOTH,
            expand=True  # ensures that the panel fill out the the parent
        )

    def do_plot(self, latest_signal_data):

        latest_signal_data = [20 * math.log((2*n)/1024, 10) for n in latest_signal_data]

        # if is first time plot, populate all data with it
        if self.isFirst:

            num_ts = self.ts_np_Y.shape[0]

            for i in range(num_ts):
                self.signal_np = np.append(self.signal_np, [latest_signal_data], axis=0)
            self.signal_np = np.asarray(self.signal_np)

        # else pop oldest data and append latest data
        else:
            for _ in range(25):
                self.signal_np = np.delete(self.signal_np, 0, axis=0)

            for _ in range(25):
                self.signal_np = np.append(self.signal_np, [latest_signal_data], axis=0)

        # clear plot
        self.ax.clear()
        self.ax.set_zlim(-100, 10)

        # plot
        cmap = cm.get_cmap("jet")
        # https://stackoverflow.com/questions/3373256/set-colorbar-range-in-matplotlib
        # cmap.set_under("b")
        # cmap.set_over("r")
        self.surf = self.ax.plot_surface(
            self.freq_bins_np_X,
            self.ts_np_Y,
            self.signal_np,
            cmap=cmap,
            antialiased=True,
            vmin=-90,
            vmax=-30
        )

        # remove the previous colorbar
        if not self.isFirst:
            self.cb.remove()

        label = [-10, -20, -30, -40, -50, -60, -70, -80, -90, -100]

        if self.is_2d == False:
            pos = "vertical"
            self.cb = self.fig.colorbar(
                self.surf,
                location="left",
                orientation=pos,
                ax=self.ax,
                shrink=0.4,
                aspect=30
            )
        else:
            pos = "horizontal"
            self.cb = self.fig.colorbar(
                self.surf,
                orientation=pos,
                ax=self.ax,
                shrink=0.4,
                aspect=30,
                pad=0
            )
        self.cb.set_ticks(label)
        self.cb.set_ticklabels([str(x) for x in label])

        # Recompute ticks for freq label
        bandwidth = self.recording.get_frequency_setting_pane().get_bandwidth()
        center_freq = self.recording.get_frequency_setting_pane().get_center_freq()
        freq_increment = bandwidth / 9
        freq_bins = []
        start_freq = center_freq - bandwidth/2
        end_freq = center_freq + bandwidth/2
        while start_freq < end_freq:
            freq_bins.append("{:.2f}".format(start_freq / 1e6))
            start_freq += freq_increment
        self.ax.set_xticklabels(freq_bins)

        # set axis label
        self.ax.set_xlabel(app_parameters.WATERFALL_PLOT_LEGEND_X)
        self.ax.set_ylabel(app_parameters.WATERFALL_PLOT_LEGEND_Y)
        self.ax.set_zlabel(app_parameters.WATERFALL_PLOT_LEGEND_Z)

        self.isFirst = False
        self.canvas.draw()
