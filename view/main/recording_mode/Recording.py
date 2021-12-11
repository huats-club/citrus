import tkinter as tk
from tkinter import ttk

from view.main.FrequencyPane import FrequencyPane
from view.main.recording_mode.RecordingSettingPane import RecordingSettingPane
from view.main.recording_mode.RecordingSpecPlot import RecordingSpecPlot
from view.main.recording_mode.RecordingWaterfallPlot import \
    RecordingWaterfallPlot


class RecordingPage(ttk.Frame):
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
        # TODO
        self.recording_plot = RecordingWaterfallPlot(
            self.recording_plot_container,
            self.controller
        )

        # Create empty plot of graph
        self.recording_plot.create_empty_3d_plot()

        # Create bottom bar of buttons to handle recording mode
        self.bottom = RecordingSettingPane(
            self.recording_plot_container,
            self,
            self.controller
        )

        # Create side panel
        self.recording_setting = FrequencyPane(
            self.container,
            self.controller
        )

    def handle_switch_spec_plot(self):
        self.recording_plot.destroy()
        # spec plot - display in first show
        self.recording_plot = RecordingSpecPlot(
            self.recording_plot_container,
            self.controller
        )
        self.recording_plot.draw()

    def handle_switch_waterfall_plot(self):
        self.recording_plot.destroy()
        self.recording_plot = RecordingWaterfallPlot(
            self.recording_plot_container,
            self.controller
        )
        self.recording_plot.create_empty_3d_plot()

    def handle_recording_start(self):
        print("start recording")

        # Start spectrum if frequency is valid and not already started
        if self.recording_setting.is_start_stop_freq_valid() and self.controller.is_recording_start == False:

            # Disable toggle to other tab
            self.parent.disable_toggle_tab()

            # disable recording setting panes
            self.bottom.disable_setting_pane()

            # disable frequency toggle
            self.recording_setting.disable_frequency_pane()

            # Set controller state variable
            self.controller.is_recording_start = True

            # get centre freq
            center_freq = self.recording_setting.get_center_freq()

            # Start process
            self.controller.start_recording_process(center_freq)

        # Else display error message
        else:
            # display error
            self.recording_setting.display_error_message(self.controller.is_recording_start)

        # Start to retrieve data to plot
        self.parent.after(100, self.get_process)

    def get_process(self):
        if self.pipe.poll(timeout=0):
            data = self.pipe.recv()
            # do plot
            self.recording_plot.do_plot(data)

        self.parent.after(500, self.get_process)

    def handle_recording_stop(self):
        print("stop recording")

        if self.controller.is_recording_start == True:

            self.controller.stop_recording_process()

            # disable recording setting panes
            self.bottom.enable_setting_pane()

            # disable frequency toggle
            self.recording_setting.enable_frequency_pane()

            # Set controller state variable
            self.controller.is_recording_start = False

            # Enable traversal of tab
            self.parent.enable_toggle_tab()

    # Provide interface for save pane to call common function
    def handle_save(self):
        self.handle_recording_save()

    def handle_recording_save(self):
        print("save recording")
