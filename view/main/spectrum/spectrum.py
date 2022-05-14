import tkinter as tk
from tkinter import ttk

import config.app_parameters as app_parameters
from view.main.frequency_pane import FrequencyPane
from view.main.select_driver_pane import SelectDriverPane
from view.main.spectrum.spectrum_plot import SpectrumPlot
from view.main.spectrum.spectrum_setting_pane import SpectrumSettingPane


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

        # Create spectrum plot
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
        self.operation_settings_pane = SpectrumSettingPane(self.spectrum_plot_container, self, controller)

        # Create select driver pane
        self.spectrum_select_driver_pane = SelectDriverPane(self.container, self.controller)

        # Create settings pane container
        self.frequency_setting_container = FrequencyPane(self.container, self.controller)

    # Required method to get the driver value input
    def get_driver_input(self):
        return self.spectrum_select_driver_pane.get_driver_input()

    # Required method to get frequency setting pane
    def get_frequency_setting_pane(self):
        return self.frequency_setting_container

    # Required method to set the error message that frequency not entered when calibration is done
    def set_invalid_calibration_message(self):
        self.enable_calibration()
        self.frequency_setting_container.display_error_message(isStarted=False)

    # Required method to set calibration in progress error
    def set_valid_calibration_message(self):
        self.frequency_setting_container.display_calibration_message()

    # Required method to set calibration completed
    def set_calibration_complete_message(self):
        self.frequency_setting_container.display_calibration_done()

    # Required method to disable calibration mode
    def disable_calibration(self):
        self.operation_settings_pane.disable_calibration_button()

    # Required method to enable calibration mode
    def enable_calibration(self):
        self.operation_settings_pane.enable_calibration_button()

    # Method to invoke display of error message when calibration not done prior to start
    def set_missing_calibration_on_start_message(self):
        self.frequency_setting_container.display_calibration_error_message()

    # Method to disable start button
    def disable_start(self):
        self.operation_settings_pane.disable_start_button()

    # Method to enable start button
    def enable_start(self):
        self.operation_settings_pane.enable_start_button()

    # Method to setup plot axis
    def setup_plot_axis(self, start_freq, center_freq, end_freq, units):
        self.spectrum_plot.set_X_axis_freq(start_freq, center_freq, end_freq, units)

    # Method to do plot
    def do_plot(self, data):
        self.spectrum_plot.do_plot(data)

    # Method is invoked to set the path of the directory to save plot images
    # NOTE: this result set to the pane might be changed by user input
    def set_spectrum_save_path(self, path):
        self.operation_settings_pane.set_save_path(path)
