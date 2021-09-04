import multiprocessing
import tkinter as tk
from tkinter import ttk

import AppParameters as app_params
from numpy.core.numeric import True_
from view.main.FrequencyPane import FrequencyPane
from view.main.SpectrumPlot import SpectrumPlot


class SpectrumPage(ttk.Frame):
    def __init__(self, parent, controller, pipe, *args, **kwargs):
        self.parent = parent
        self.controller = controller
        self.pipe = pipe

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
        self.bottom_container = SpectrumSettingPane(self.spectrum_plot_container, self, controller)

        # Create settings pane container
        self.spectrum_setting_container = FrequencyPane(self.container, self.controller)

        # Start to retrieve data to plot
        self.parent.after(100, self.getProcess)

    def getProcess(self):

        if self.pipe.poll(timeout=0):
            data = self.pipe.recv()
            print(data)

            # do plot
            self.spectrum_plot.doPlot(data)

        self.parent.after(500, self.getProcess)

    def handle_spectrum_start(self):

        # Start spectrum if frequency is valid and not already started
        if self.spectrum_setting_container.is_start_stop_freq_valid() and self.controller.isSpectrumStart == False:

            print("Spectrum page - start pressed")

            # get centre freq
            center_freq = self.spectrum_setting_container.get_center_freq()

            # Set plot bounds
            self.spectrum_plot.setXAxisBound(self.spectrum_setting_container.get_start_freq(),
                                             self.spectrum_setting_container.get_stop_freq())

            # Start spectrum
            self.controller.start_spectrum_process(center_freq)

            # Disable setting of frequency in frequency pane
            self.spectrum_setting_container.disable_frequency_pane()

            # Set controller state variable
            self.controller.isSpectrumStart = True

        # Else display error message
        else:
            # display error
            self.spectrum_setting_container.displayErrorMessage(self.controller.isSpectrumStart)

    def handle_spectrum_stop(self):

        if self.controller.isSpectrumStart == True:

            print("Spectrum page - stop pressed")

            # Stop spectrum
            self.controller.stop_spectrum_process()

            # Enable setting of frequency in frequency pane
            self.spectrum_setting_container.enable_frequency_pane()

            # Set controller state variable
            self.controller.isSpectrumStart = False


class SpectrumSettingPane(tk.Frame):
    def __init__(self, parent, spectrum, controller, *args, **kwargs):

        self.parent = parent
        self.controller = controller
        self.spectrum = spectrum

        super().__init__(self.parent, *args, **kwargs)
        self.pack(
            side=tk.BOTTOM
        )

        # Start button
        self.start_button = ttk.Button(
            self,
            style="primary.TButton",
            text="Start",
            command=self.spectrum.handle_spectrum_start
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
            text="Stop",
            command=self.spectrum.handle_spectrum_stop
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
