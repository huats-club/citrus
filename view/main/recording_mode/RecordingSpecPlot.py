import math
import tkinter as tk
import warnings
from tkinter import ttk

import matplotlib.backends.backend_tkagg as tkmatplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
from matplotlib import cm

warnings.simplefilter("ignore", UserWarning)

first = False


class RecordingSpecPlot(ttk.Frame):
    def __init__(self, parent, controller, recording, center_freq=740.3e6, bandwidth=20e6, *args, **kwargs):
        self.parent = parent
        self.controller = controller
        self.recording = recording

        super().__init__(self.parent, *args, **kwargs)
        self.pack(
            padx=5,
            pady=5,
            side=tk.BOTTOM,
            fill=tk.BOTH,
            expand=True  # ensures that the panel file out the the parent
        )

        # flag to indicate first data
        self.isFirst = True

        # incre
        self.incre = 1

        # generate xticks
        xticks_exact = [center_freq - bandwidth/2, center_freq, center_freq + bandwidth/2]
        self.xticks_label = [x/1e6 for x in xticks_exact]

        # prepare z signal data store
        self.signal_datastore_np = np.full((150, 2048), -100)

        global first
        first = True
        self.create_empty_plot()
        self.draw()
        first = False

    def do_plot(self, latest_signal_data):
        # self.latest_signal_data = latest_signal_data
        self.latest_signal_data = [20 * math.log((2*n)/1024, 10) for n in latest_signal_data]

        # if is first time plot, populate all data with it
        if self.isFirst:
            self.signal_datastore_np = np.zeros((0, 2048))
            for i in range(150):
                self.signal_datastore_np = np.append(self.signal_datastore_np, [self.latest_signal_data], axis=0)
            self.signal_datastore_np = np.asarray(self.signal_datastore_np)

            self.isFirst = False

        # else pop oldest data and append latest data
        else:

            # Do bulk concat
            self.signal_datastore_np = np.concatenate(
                (
                    np.repeat([np.array(self.latest_signal_data)], 10, axis=0),
                    self.signal_datastore_np
                ),
                axis=0
            )

            # Do bulk delete
            self.signal_datastore_np = self.signal_datastore_np[:-10, :]

            start_freq = self.recording.recording_setting.get_start_freq()
            end_freq = self.recording.recording_setting.get_stop_freq()
            center_freq = 0.5 * (float(start_freq) + float(end_freq))
            self.xticks_label = [str(start_freq) + " MHz", str(center_freq) + " MHz", str(end_freq) + " MHz"]
            self.ax.xaxis.set_major_formatter(ticker.FixedFormatter((self.xticks_label)))

        self.draw()

    def draw(self):
        # plot
        self.waterfall2d = self.ax.imshow(
            self.signal_datastore_np, cmap=cm.get_cmap("jet"),
            interpolation='bicubic', aspect='auto')

        global first
        if first:
            self.cb = self.fig.colorbar(
                self.waterfall2d,
                location="bottom",
                orientation="horizontal",
                ax=self.ax,
                shrink=0.4,
                aspect=30,
                pad=0.08
            )
            first = False

        else:
            self.cb.remove()
            self.cb = self.fig.colorbar(
                self.waterfall2d,
                location="bottom",
                orientation="horizontal",
                ax=self.ax,
                shrink=0.4,
                aspect=30,
                pad=0.08
            )
            # self.cb.set_clim(min(self.latest_signal_data), max(self.latest_signal_data))
            try:
                self.cb.mappable.set_clim(
                    vmin=-120,
                    vmax=-20)  # this works
                self.cb.draw_all()
            except AttributeError:
                pass

        self.ax.set_yticks([])
        self.ax.xaxis.set_major_locator(ticker.LinearLocator(numticks=3))
        self.ax.xaxis.set_major_formatter(ticker.FixedFormatter((self.xticks_label)))

        self.canvas.draw()

    def create_empty_plot(self):

        # https://towardsdatascience.com/cyberpunk-style-with-matplotlib-f47404c9d4c5

        plt.style.use("seaborn-dark")

        for param in ['figure.facecolor', 'axes.facecolor', 'savefig.facecolor']:
            plt.rcParams[param] = '#212946'  # bluish dark grey

        for param in ['text.color', 'axes.labelcolor', 'xtick.color', 'ytick.color']:
            plt.rcParams[param] = '0.9'  # very light grey

        plt.rcParams['font.size'] = 12

        self.colors = [
            '#08F7FE',  # teal/cyan
            '#FE53BB',  # pink
            '#F5D300',  # yellow
            '#00ff41',  # matrix green
        ]

        self.fig = plt.figure()
        self.fig.tight_layout()
        self.ax = self.fig.add_subplot()

        # Change later to line plot+ with mock data
        self.canvas = tkmatplotlib.FigureCanvasTkAgg(
            self.fig,
            self
        )
        self.canvas.get_tk_widget().pack(
            side=tk.TOP,
            fill=tk.BOTH,
            expand=True  # ensures that the panel file out the the parent
        )

        self.ax.set_autoscaley_on(True)

    def save(self, filepath):
        self.fig.savefig(filepath)
