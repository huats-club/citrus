import math
import tkinter as tk
from tkinter import ttk

import config.app_parameters as app_parameters
import matplotlib.backends.backend_tkagg as tkmatplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
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
        self.ax = plt.subplot(111, projection='3d')

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

    def set_2d(self):
        self.fig = plt.figure()
        self.fig.tight_layout()
        self.ax = self.fig.add_subplot()
        self.canvas.get_tk_widget().destroy()
        self.canvas = tkmatplotlib.FigureCanvasTkAgg(
            self.fig,
            self
        )
        self.canvas.get_tk_widget().pack(
            side=tk.TOP,
            fill=tk.BOTH,
            expand=True  # ensures that the panel fill out the the parent
        )
        self.is_2d = True
        self.isFirst = True

    def do_plot(self, latest_signal_data, start_freq, center_freq, end_freq, bandwidth):

        # generate frequency bins
        freq_increment = (bandwidth / 2048) / 1e6
        freq_bins = []

        while start_freq < end_freq:
            freq_bins.append(start_freq)
            start_freq += freq_increment
        freq_bins_np = np.asarray(freq_bins)

        # generate (initial) timestamp marker
        # FIX: more points, nearer the peaks, to form a continuous bar
        ts_np = np.arange(500)

        # prepare 2d x,y data
        freq_bins_np_X, ts_np_Y = np.meshgrid(freq_bins_np, ts_np)

        # Prepare latest data
        latest_signal_data = [20 * math.log((2*n)/1024, 10) for n in latest_signal_data]

        # Reverse back to original data
        if self.is_2d == True:
            self.signal_np = self.signal_np[::-1]

        # if is first time plot, populate all data with it
        if self.isFirst:
            num_ts = self.ts_np_Y.shape[0]

            for _ in range(num_ts):
                self.signal_np = np.append(self.signal_np, [latest_signal_data], axis=0)
            self.signal_np = np.asarray(self.signal_np)

        # else pop oldest data and append latest data
        else:
            for _ in range(25):
                self.signal_np = np.delete(self.signal_np, 0, axis=0)

            for _ in range(25):
                self.signal_np = np.append(self.signal_np, [latest_signal_data], axis=0)

        # Reverse to display from new to old down
        if self.is_2d == True:
            self.signal_np = self.signal_np[::-1]

        # clear plot
        self.ax.clear()

        if self.is_2d == False:

            # plot
            cmap = cm.get_cmap("jet")
            # https://stackoverflow.com/questions/3373256/set-colorbar-range-in-matplotlib
            # cmap.set_under("b")
            # cmap.set_over("r")
            self.surf = self.ax.plot_surface(
                freq_bins_np_X,
                ts_np_Y,
                self.signal_np,
                cmap=cmap,
                antialiased=True,
                vmin=-90,
                vmax=-30
            )

            # remove the previous colorbar
            if not self.isFirst:
                self.cb.remove()

            label = [-10, -20, -30, -40, -50, -60, -70, -80, -90, -100, -110]

            pos = "vertical"
            self.cb = self.fig.colorbar(
                self.surf,
                location="left",
                orientation=pos,
                ax=self.ax,
                shrink=0.4,
                aspect=30
            )
            self.cb.set_ticks(label)
            self.cb.set_ticklabels([str(x) for x in label])

        else:
            self.waterfall2d = self.ax.imshow(
                self.signal_np, cmap=cm.get_cmap("jet"),
                interpolation='bicubic', vmin=-90, vmax=-30)

            if self.isFirst:
                self.fig.colorbar(
                    self.waterfall2d,
                    location="bottom",
                    orientation="horizontal",
                    ax=self.ax,
                    shrink=0.4,
                    aspect=30,
                    pad=0.08
                )
                self.isFirst = False

            self.ax.set_yticks([])
            xticks_exact = [center_freq - bandwidth/2, center_freq - bandwidth/4,
                            center_freq,  center_freq + bandwidth/4, center_freq + bandwidth/2]
            xticks_label = [x/1e6 for x in xticks_exact]
            self.ax.xaxis.set_major_locator(ticker.LinearLocator(numticks=5))
            self.ax.xaxis.set_major_formatter(ticker.FixedFormatter((xticks_label)))

        # set axis label
        self.ax.set_xlabel(app_parameters.WATERFALL_PLOT_LEGEND_X)
        self.ax.set_ylabel(app_parameters.WATERFALL_PLOT_LEGEND_Y)

        if self.is_2d == False:
            self.ax.set_zlabel(app_parameters.WATERFALL_PLOT_LEGEND_Z)

        self.isFirst = False
        self.canvas.draw()

    def save(self, filepath):
        self.fig.savefig(filepath)
