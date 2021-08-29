import tkinter as tk
from tkinter import ttk

import AppParameters as app_params
import matplotlib.backends.backend_tkagg as tkmatplotlib
import matplotlib.pyplot as plt
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

        # Change later to line plot + with mock data
        self.plot = tkmatplotlib.FigureCanvasTkAgg(
            self.figure,
            self
        )
        self.plot.get_tk_widget().pack(
            side=tk.TOP,
            fill=tk.BOTH,
            expand=True  # ensures that the panel fill out the the parent
        )

        self.ax.set_xlabel(
            app_params.SPECTRUM_PLOT_LEGEND_X
        )
        self.ax.set_ylabel(
            app_params.SPECTRUM_PLOT_LEGEND_Y
        )

    def doPlot(self, dataframe):

        # df = pd.DataFrame({'A': [1, 3, 9, 5, 2, 1, 1]})

        # Do plot
        dataframe.plot(marker='o', ax=self.ax, color=self.colors)

        # Create glow
        n_lines = 10
        diff_linewidth = 1.05
        alpha_value = 0.03
        for n in range(1, n_lines+1):
            dataframe.plot(marker='o',
                           linewidth=2+(diff_linewidth*n),
                           alpha=alpha_value,
                           legend=False,
                           ax=self.ax,
                           color=self.colors)

    def setXAxisBound(self, xlow, xhigh):
        self.ax.set_xlim(xlow, xhigh)

    def setYAxisBound(self, ylow, yhigh):
        self.ax.set_ylim(ylow, yhigh)
