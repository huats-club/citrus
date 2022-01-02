import tkinter as tk
from tkinter import ttk

from app_parameters import app_parameters
from view.main.FrequencyPane import FrequencyPane
from view.main.SelectDriverPane import SelectDriverPane
from view.main.spectrum_mode.SpectrumPlot import SpectrumPlot
from view.main.spectrum_mode.SpectrumSettingPane import SpectrumSettingPane


class SpectrumPage(ttk.Frame):
    def __init__(self, parent, controller, pipe, *args, **kwargs):
        self.parent = parent
        self.controller = controller
        self.pipe = pipe

        self.save_path = self.controller.session.get_session_workspace_path()

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

        # Start to retrieve data to plot
        self.parent.after(100, self.get_process)

    def get_process(self):
        if self.pipe.poll(timeout=0):
            data = self.pipe.recv()
            # do plot
            self.spectrum_plot.do_plot(data)

        self.parent.after(500, self.get_process)

    def handle_spectrum_start(self):

        # Start spectrum if frequency is valid and not already started
        if self.spectrum_setting_container.is_start_stop_freq_valid() and self.controller.is_spectrum_start == False:

            # Disable toggle to other tab
            self.parent.disable_toggle_tab()

            # get freqs
            start_freq = self.spectrum_setting_container.get_start_freq()
            center_freq = self.spectrum_setting_container.get_center_freq()
            end_freq = self.spectrum_setting_container.get_stop_freq()

            # get bandwidth
            bandwidth = self.spectrum_setting_container.get_bandwidth()

            # Set plot bounds
            units = self.spectrum_setting_container.get_freq_units()
            self.spectrum_plot.set_X_axis_freq(start_freq, center_freq, end_freq, units)

            # Start spectrum
            driver_name = self.spectrum_select_driver_pane.get_driver_input()
            self.controller.start_spectrum_process(driver_name, center_freq, bandwidth)

            # Disable setting of frequency in frequency pane
            self.spectrum_setting_container.disable_frequency_pane()

            # Set controller state variable
            self.controller.is_spectrum_start = True

        # Else display error message
        else:
            # display error
            self.spectrum_setting_container.display_error_message(self.controller.is_spectrum_start)

    def handle_spectrum_stop(self):

        if self.controller.is_spectrum_start == True:
            # Stop spectrum
            self.controller.stop_spectrum_process()

            # Enable setting of frequency in frequency pane
            self.spectrum_setting_container.enable_frequency_pane()

            # Set controller state variable
            self.controller.is_spectrum_start = False

            # Enable traversal of tab
            self.parent.enable_toggle_tab()

    def update_save_path(self, path):
        self.save_path = path

    # Provide interface for save pane to call common function
    def handle_save(self):
        self.handle_spectrum_save()

    def handle_spectrum_save(self):
        count = self.controller.session.get_current_spectrum_plot_num()
        filepath = f"{self.save_path}/spectrum_{count}"
        self.controller.session.increment_spectrum_plot_num()
        self.spectrum_plot.save(filepath)
