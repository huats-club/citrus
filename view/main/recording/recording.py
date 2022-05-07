import tkinter as tk
from tkinter import ttk
from view.main.frequency_pane import FrequencyPane
from view.main.recording.recording_setting_pane import RecordingSettingPane
from view.main.recording.recording_waterfall_plot import RecordingWaterfallPlot
from view.main.select_driver_pane import SelectDriverPane


class RecordingPage(ttk.Frame):
    def __init__(self, parent, controller, *args, **kwargs):
        self.parent = parent
        self.controller = controller

        # Flag to indicate current 2d/3d
        self.is_3d = True

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

        # Waterfall plot - display in first show
        self.recording_plot = RecordingWaterfallPlot(
            self.recording_plot_container,
            self.controller,
            self
        )

        # Create empty plot of graph
        self.recording_plot.create_empty_3d_plot()

        # Create bottom bar of buttons to handle recording mode
        self.bottom = RecordingSettingPane(
            self.recording_plot_container,
            self,
            self.controller
        )

        # Create select driver panel
        self.select_driver_pane = SelectDriverPane(self.container, self.controller)

        # Create side panel
        self.recording_setting = FrequencyPane(
            self.container,
            self.controller
        )

    def handle_switch_spec_plot(self):
        self.recording_plot.destroy()
        self.recording_plot = RecordingWaterfallPlot(
            self.recording_plot_container,
            self.controller,
            self
        )
        self.recording_plot.create_empty_3d_plot()
        self.recording_plot.set_2d()
        self.is_3d = False

    def handle_switch_waterfall_plot(self):
        self.recording_plot.destroy()
        self.recording_plot = RecordingWaterfallPlot(
            self.recording_plot_container,
            self.controller,
            self
        )
        self.recording_plot.create_empty_3d_plot()
        self.is_3d = True
