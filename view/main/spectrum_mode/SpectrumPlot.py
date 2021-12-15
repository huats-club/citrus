import tkinter as tk
from tkinter import ttk

import matplotlib.backends.backend_tkagg as tkmatplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd
from app_parameters import app_parameters


class SpectrumPlot(ttk.Frame):
    def __init__(self, parent, controller, *args, **kwargs):
        self.parent = parent
        self.controller = controller

        super().__init__(self.parent, *args, **kwargs)
        self.pack(
            padx=10,
            pady=10,
            side=tk.TOP,
            fill=tk.BOTH,
            expand=True  # ensures that the panel file out the the parent
        )

    def create_empty_plot(self):
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

        self.figure = plt.Figure(figsize=(5, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.ax.grid(color='#2A3459')  # bluish dark grey, but slightly lighter than background

        # Change later to line plot+ with mock data
        self.canvas = tkmatplotlib.FigureCanvasTkAgg(
            self.figure,
            self
        )
        self.canvas.get_tk_widget().pack(
            side=tk.TOP,
            fill=tk.BOTH,
            expand=True  # ensures that the panel fill out the the parent
        )

        self.ax.set_xlabel(
            app_parameters.SPECTRUM_PLOT_LEGEND_X,
            labelpad=20,
            fontsize="large",
            fontweight="medium"
        )
        self.ax.set_ylabel(
            app_parameters.SPECTRUM_PLOT_LEGEND_Y,
            labelpad=20,
            fontsize="large",
            fontweight="medium"
        )

    def do_plot(self, data):

        self.figure.clear()
        self.ax = self.figure.add_subplot(111)
        self.ax.grid(color='#2A3459')  # bluish dark grey, but slightly lighter than background

        self.canvas.draw_idle()
        self.ax.set_xlabel(
            app_parameters.SPECTRUM_PLOT_LEGEND_X,
            labelpad=20,
            fontsize="large",
            fontweight="medium"
        )
        self.ax.set_ylabel(
            app_parameters.SPECTRUM_PLOT_LEGEND_Y,
            labelpad=20,
            fontsize="large",
            fontweight="medium"
        )

        # get data to plot
        df = pd.DataFrame(data, columns=['power'])

        # plot data
        self.ax.plot(df['power'], linewidth=1)
        df.plot(marker='', ax=self.ax, color=self.colors)

        # change axis values label
        self.ax.xaxis.set_major_locator(ticker.LinearLocator(numticks=3))
        self.ax.xaxis.set_major_formatter(ticker.FixedFormatter((self.freq_label_list)))

        # self.ax.set_autoscaley_on(True)
        self.ax.set_ylim(-140, 0)

    def set_X_axis_freq(self, start_freq, centre_freq, end_freq, units):

        # generate list of label
        if units == app_parameters.SPECTRUM_PLOT_UNITS_PREFIX_KILO_X:
            self.freq_label_list = [start_freq, centre_freq / pow(10, 3), end_freq]

        elif units == app_parameters.SPECTRUM_PLOT_UNITS_PREFIX_MEGA_X:
            self.freq_label_list = [start_freq, centre_freq / pow(10, 6), end_freq]

        else:
            self.freq_label_list = [start_freq, centre_freq / pow(10, 9), end_freq]

        # process to string
        self.freq_label_list = [f"{x} {units}Hz" for x in self.freq_label_list]

    def save(self, filepath):
        self.figure.savefig(filepath)
