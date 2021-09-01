import tkinter as tk
from tkinter import ttk

import AppParameters as app_params
import matplotlib.backends.backend_tkagg as tkmatplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


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

    def createEmptyPlot(self):
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

        self.ax.set_autoscaley_on(True)

        self.ax.set_xlabel(
            app_params.SPECTRUM_PLOT_LEGEND_X
        )
        self.ax.set_ylabel(
            app_params.SPECTRUM_PLOT_LEGEND_Y
        )

    def doPlot(self, data):

        self.figure.clear()
        self.ax = self.figure.add_subplot(111)
        self.ax.grid(color='#2A3459')  # bluish dark grey, but slightly lighter than background

        self.canvas.draw_idle()
        self.ax.set_xlabel(
            app_params.SPECTRUM_PLOT_LEGEND_X
        )
        self.ax.set_ylabel(
            app_params.SPECTRUM_PLOT_LEGEND_Y
        )

        # self.setXAxisBound(self.xlow, self.xhigh)
        # self.setYAxisBound(-40, 0)
        df = pd.DataFrame(data, columns=['power'])

        self.ax.plot(df['power'], linewidth=1)

        # Do plot
        df.plot(marker='', ax=self.ax, color=self.colors)

    def setXAxisBound(self, xlow, xhigh):
        self.xlow = xlow
        self.xhigh = xhigh

    def setYAxisBound(self, ylow, yhigh):
        self.ax.set_ylim(ylow, yhigh)
