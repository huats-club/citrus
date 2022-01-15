import tkinter as tk
from multiprocessing import Pipe
from tkinter import ttk

import numpy as np
from model.ReplayHandler import ReplayHandler
from view.main.recording_mode.RecordingSpecPlot import RecordingSpecPlot
from view.main.recording_mode.RecordingWaterfallPlot import \
    RecordingWaterfallPlot
from view.main.replay_mode.ReplaySettingPane import ReplaySettingPane
from view.main.spectrum_mode.SpectrumPlot import SpectrumPlot


class ReplayPage(ttk.Frame):
    def __init__(self, parent, controller, *args, **kwargs):
        self.parent = parent
        self.controller = controller

        super().__init__(self.parent,  *args, **kwargs)
        self.pack(
            padx=10,
            pady=10,
            fill=tk.BOTH,
            expand=True  # ensures fill out the the parent
        )

        # Create main container
        self.container = ttk.Frame(self)
        self.container.pack(
            padx=4,
            pady=4,
            fill=tk.BOTH,
            expand=True
        )

        # Create plot container
        self.plot_container = tk.Frame(
            self.container
        )
        self.plot_container.pack(
            padx=10,
            pady=10,
            side=tk.TOP,
            fill=tk.BOTH,
            expand=True
        )

        # Create plot object
        self.plot = RecordingWaterfallPlot(self.plot_container, self.controller, self)
        self.plot.create_empty_3d_plot()  # first plot

        # Bottom container
        self.settings_container = tk.Frame(
            self.container
        )
        self.settings_container.pack(
            padx=10,
            pady=10,
            side=tk.BOTTOM,
            fill=tk.BOTH
        )

        # Create replay settings
        self.replay_settings_pane = ReplaySettingPane(self.settings_container, self, self.controller)

    def start_replay(self, filepath):

        # get filepath to load and validate
        print(f"Replay filepath loaded: {filepath}")

        # Load data
        try:
            data = np.load(filepath)
        except OSError:
            print("Can't load data file for replay")
            return

        # TODO: create pipe to feed data
        self.pipe_replay, pipe_handler = Pipe(True)
        self.replay_coverage = ReplayHandler(data, pipe_handler)

        # Start to feed data to plot
        self.parent.after(100, self.handle_data_run)

    def handle_data_run(self):

        # get radiobutton which type of plot to display and do the plot
        # NOTE: no checking is done to validate if file is matching the correct plot type!!
        if self.replay_settings_pane.get_mode_selected() == self.replay_settings_pane.SELECTED_3D:
            print("3D Plot")

        elif self.replay_settings_pane.get_mode_selected() == self.replay_settings_pane.SELECTED_2D:
            print("2D Plot")

        else:
            print("Spectrum Plot")

        self.parent.after(1000, self.handle_data_run)

    def handle_switch_2d_plot(self):
        self.plot.destroy()
        self.plot = RecordingSpecPlot(
            self.plot_container,
            self.controller,
            self
        )
        self.plot.draw()

    def handle_switch_3d_plot(self):
        self.plot.destroy()
        self.plot = RecordingWaterfallPlot(self.plot_container, self.controller,
                                           self)
        self.plot.create_empty_3d_plot()

    def handle_switch_spectrum_plot(self):
        self.plot.destroy()
        self.plot = SpectrumPlot(self.plot_container, self.controller)
        self.plot.create_empty_plot()
