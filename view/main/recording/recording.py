import tkinter as tk
from tkinter import ttk
from urllib.parse import parse_qs

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
        self.operation_settings_pane = RecordingSettingPane(
            self.recording_plot_container,
            self,
            self.controller
        )

        # Create select driver panel
        self.recording_select_driver_pane = SelectDriverPane(self.container, self.controller)

        # Create side panel
        self.frequency_setting_container = FrequencyPane(self.container, self.controller)

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

    # Method is invoked to update the plot
    def do_plot(self, data):
        self.recording_plot.do_plot(data)

    # Required method to get the driver value input
    def get_driver_input(self):
        return self.recording_select_driver_pane.get_driver_input()

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

    # Method is invoked to set the path of the directory to save plot images
    # NOTE: this result set to the pane might be changed by user input
    def set_recording_save_path(self, path):
        self.operation_settings_pane.set_save_path(path)

    def get_save_path(self):
        return self.operation_settings_pane.get_save_path()

    # Method is invoked to save path
    def save_plot(self, path):
        self.recording_plot.save(path)
