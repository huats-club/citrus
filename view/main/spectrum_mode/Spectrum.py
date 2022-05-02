import tkinter as tk
from multiprocessing import Pipe
from tkinter import ttk

import numpy as np
from app_parameters import app_parameters
from model.CalibrateHandler import CalibrateHandler
from model.ConfigPacker import ConfigParser
from view.main.FrequencyPane import FrequencyPane
from view.main.SelectDriverPane import SelectDriverPane
from view.main.spectrum_mode.SpectrumPlot import SpectrumPlot
from view.main.spectrum_mode.SpectrumSettingPane import SpectrumSettingPane


class SpectrumPage(ttk.Frame):
    def __init__(self, parent, controller, pipe, session, *args, **kwargs):
        self.parent = parent
        self.controller = controller
        self.pipe = pipe
        self.session = session

        self.save_path = self.session.get_session_workspace_path()

        # Store data for logging later on end
        self.run_count = 1
        self.data_store = []

        # Calibrate data
        self.calibrate_data = None
        self.is_calibrating = False

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

    def handle_calibrate(self):
        if self.is_calibrating == False:
            self.bottom_container.disable_calibration_button()
            self.is_calibrating = True
            print("start spectrum mode calibration")

            # get centre freq
            center_freq = self.spectrum_setting_container.get_center_freq()

            # get bandwidth
            bandwidth = self.spectrum_setting_container.get_bandwidth()

            # check if calibration can be done
            if center_freq == "" or bandwidth == "":
                self.spectrum_setting_container.display_error_message(isStarted=False)
                return

            # Start process
            driver_name = self.spectrum_select_driver_pane.get_driver_input()
            c = CalibrateHandler()
            self.pipe_here, pipe_calibrate = Pipe(True)
            c.start(driver_name, pipe_calibrate, center_freq, bandwidth)

            self.parent.after(100, self.get_calibrate)
            self.spectrum_setting_container.display_calibration_message()

    def get_calibrate(self):
        if self.pipe_here.poll(timeout=0):
            data = self.pipe_here.recv()
            self.calibrate_data = data
            self.is_calibrating = False

        if self.is_calibrating == True:
            self.parent.after(50, self.get_calibrate)
        else:
            self.spectrum_setting_container.display_calibration_done()
            self.bottom_container.enable_calibration_button()
            self.is_calibrating = False
            print("complete spectrum mode calibration")

    def handle_spectrum_start(self):

        if self.calibrate_data == None:
            self.spectrum_setting_container.display_calibration_error_message()
            return

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

            # Start to retrieve data to plot
            self.parent.after(100, self.get_process)

        # Else display error message
        else:
            # display error
            self.spectrum_setting_container.display_error_message(self.controller.is_spectrum_start)

    def get_process(self):
        if self.pipe.poll(timeout=0):

            data = self.pipe.recv()

            average_of_all_calibrate = np.average(data)
            data = np.subtract(data, self.calibrate_data)
            data = data + average_of_all_calibrate

            # do plot
            x = data.tolist()

            for idx in range(len(x)):
                if x[idx] < 0:
                    x[idx] = average_of_all_calibrate

            # do plot
            self.spectrum_plot.do_plot(x)

            # append data for storage at end of run
            self.data_store.append(x)

        self.parent.after(500, self.get_process)

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

            # Save data to file and log out freq used
            output_data_file = fr"{self.save_path}/spectrum_data_{self.run_count}"
            np.save(output_data_file, np.array(self.data_store))
            output_log_file = fr"{self.save_path}/spectrum_log_{self.run_count}.txt"
            with open(output_log_file, "w") as f:
                start_freq = self.spectrum_setting_container.get_start_freq()
                end_freq = self.spectrum_setting_container.get_stop_freq()
                units = self.spectrum_setting_container.get_freq_units()
                f.write(f"Start freq: {start_freq}\n")
                f.write(f"End freq: {end_freq}\n")
                f.write(f"Units: {units}")
            self.data_store = []
            self.run_count += 1

    def update_save_path(self, path):
        self.save_path = path

    def get_driver(self):
        return self.spectrum_select_driver_pane.get_driver_input()

    # Provide interface for save pane to call common function
    def handle_save(self):
        self.handle_spectrum_save()

    def handle_spectrum_save(self):
        count = self.controller.session.get_current_spectrum_plot_num()
        filepath = f"{self.save_path}/spectrum_{count}"
        self.controller.session.increment_spectrum_plot_num()
        self.spectrum_plot.save(filepath)

    def setup_page_from_config(self, config, path):
        start_freq, center_freq, end_freq, driver = ConfigParser().parse_spectrum_config(config)
        self.spectrum_setting_container.set_start_freq(start_freq)
        self.spectrum_setting_container.set_center_freq(center_freq)
        self.spectrum_setting_container.set_stop_freq(end_freq)
        self.spectrum_select_driver_pane.set_driver_input(driver)

        # self.bottom_container.set_save_path(path)
        # self.save_path = path

        # Set save path
        # self.save_pane.set_filepath(self.session.get_session_workspace_path())
