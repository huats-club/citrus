import tkinter as tk
from tkinter import ttk

import AppParameters as app_params
from view.main.FrequencyPane import FrequencyPane
from view.main.SpectrumPlot import SpectrumPlot


class SpectrumPage(ttk.Frame):
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
            padx=10,
            pady=10,
            fill=tk.BOTH,
            expand=True
        )

        # Create spectrum analyzer plot container
        self.spectrum_plot_container = tk.Frame(
            self.container
        )
        self.spectrum_plot_container.pack(
            padx=10,
            pady=10,
            side=tk.LEFT,
            fill=tk.BOTH,
            expand=True
        )

        self.spectrum_plot = SpectrumPlot(
            self.spectrum_plot_container,
            self.controller,
            width=0.6*app_params.APP_WIDTH
        )

        # Create empty plot of graph
        self.spectrum_plot.createEmptyPlot()

        # Create bottom bar for start, stop and save
        self.bottom_container = SpectrumSettingPane(self.spectrum_plot_container, controller)

        # Create settings pane container
        self.spectrum_setting_container = FrequencyPane(self.container, self.controller)


class SpectrumSettingPane(tk.Frame):
    def __init__(self, parent, controller, *args, **kwargs):

        self.parent = parent
        self.controller = controller

        super().__init__(self.parent, *args, **kwargs)
        self.pack(
            side=tk.BOTTOM
        )

        # Start button
        self.start_button = ttk.Button(
            self,
            style="primary.TButton",
            text="Start"
        )
        self.start_button.pack(
            side=tk.LEFT,
            padx=10,
            pady=(20, 0)
        )

        # Stop button
        self.stop_button = ttk.Button(
            self,
            style="primary.TButton",
            text="Stop"
        )
        self.stop_button.pack(
            side=tk.LEFT,
            padx=10,
            pady=(20, 0)
        )

        # Save button
        self.save_button = ttk.Button(
            self,
            style="primary.TButton",
            text="Save"
        )
        self.save_button.pack(
            side=tk.RIGHT,
            padx=10,
            pady=(20, 0)
        )

        self.pack(
            side=tk.BOTTOM,
            anchor=tk.CENTER
        )
