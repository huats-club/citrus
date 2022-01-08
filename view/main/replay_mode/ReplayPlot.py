import tkinter as tk
from tkinter import ttk

import matplotlib.backends.backend_tkagg as tkmatplotlib
import matplotlib.pyplot as plt
import numpy as np
from app_parameters import app_parameters
from matplotlib import cm


class ReplayPlot(ttk.Frame):
    def __init__(self, parent, controller, *args, **kwargs):
        self.parent = parent
        self.controller = controller

        super().__init__(self.parent, *args, **kwargs)
        self.pack(
            padx=5,
            pady=5,
            side=tk.TOP,
            fill=tk.BOTH,
            expand=True  # ensures that the panel file out the the parent
        )

        self.create_empty_spectrum_2d_plot()

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

        self.ax.set_autoscaley_on(True)

    def create_empty_spectrum_2d_plot(self):

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
