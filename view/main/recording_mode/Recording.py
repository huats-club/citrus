import tkinter as tk
from tkinter import ttk

from view.main.FrequencyPane import FrequencyPane
from view.main.recording_mode.RecordingPlot import RecordingPlot
from view.main.recording_mode.RecordingSettingPane import RecordingSettingPane


class RecordingPage(ttk.Frame):
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

        # Create recording plot container
        self.recording_plot_container = tk.Frame(
            self.container
        )
        self.recording_plot_container.pack(
            padx=10,
            pady=10,
            side=tk.LEFT,
            fill=tk.BOTH,
            expand=True
        )

        self.recording_plot = RecordingPlot(
            self.recording_plot_container,
            self.controller
        )

        # Create empty plot of graph
        self.recording_plot.create_empty_plot()

        # Create bottom bar of buttons to handle recording mode
        self.bottom_container = RecordingSettingPane(
            self.recording_plot_container,
            self,
            self.controller
        )

        # Create side panel
        self.recording_setting_container = FrequencyPane(
            self.container,
            self.controller
        )

    def handle_recording_start(self):
        print("start recording")

    def handle_recording_stop(self):
        print("stop recording")

    def handle_recording_save(self):
        print("save recording")
