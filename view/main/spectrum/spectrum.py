import tkinter as tk
from tkinter import ttk

import config.app_parameters as app_parameters
from view.main.frequency_pane import FrequencyPane
from view.main.select_driver_pane import SelectDriverPane
from view.main.spectrum.spectrum_setting_pane import SpectrumSettingPane
from view.main.spectrum.spectrum_plot import SpectrumPlot


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
            width=0.6*app_parameters.APP_WIDTH
        )

        # Create empty plot of graph
        self.spectrum_plot.create_empty_plot()

        # Create bottom bar for start, stop and save
        self.bottom_container = SpectrumSettingPane(self.spectrum_plot_container, self, controller)

        # Create select driver pane
        self.spectrum_select_driver_pane = SelectDriverPane(self.container, self.controller)

        # Create settings pane container
        self.spectrum_setting_container = FrequencyPane(self.container, self.controller)

    def get_driver(self):
        return self.spectrum_select_driver_pane.get_driver_input()
