import tkinter as tk
from tkinter import ttk


class RecordingSettingPane(tk.Frame):
    def __init__(self, parent, recording, controller, *args, **kwargs):

        self.parent = parent
        self.controller = controller
        self.recording = recording

        self.SELECTED_2D = 1
        self.SELECTED_3D = 0

        super().__init__(self.parent, *args, **kwargs)
        self.pack(
            side=tk.BOTTOM,
            anchor=tk.CENTER
        )

        # Start button
        self.start_button = ttk.Button(
            self,
            style="primary.Outline.TButton",
            text="Start",
            command=self.recording.handle_recording_start
        )
        self.start_button.pack(
            side=tk.LEFT,
            padx=10,
            pady=(20, 0)
        )

        # Stop button
        self.stop_button = ttk.Button(
            self,
            style="primary.Outline.TButton",
            text="Stop",
            command=self.recording.handle_recording_stop
        )
        self.stop_button.pack(
            side=tk.LEFT,
            padx=10,
            pady=(20, 0)
        )

        # Save button
        self.save_button = ttk.Button(
            self,
            style="primary.Outline.TButton",
            text="Save",
            command=self.recording.handle_recording_save
        )
        self.save_button.pack(
            side=tk.LEFT,
            padx=10,
            pady=(20, 0)
        )

        # Toggle 2D / 3D view - radio buttons
        self.dimension_selector_frame = ttk.Frame(
            self,
            relief=tk.GROOVE
        )
        self.dimension_selector_frame.pack(
            side=tk.RIGHT,
            padx=10,
            pady=(20, 0)
        )

        self.dimension_selector_label = ttk.Label(
            self.dimension_selector_frame,
            text="Select dimension: "
        )
        self.dimension_selector_label.pack(
            side=tk.LEFT,
            padx=10,
            pady=5
        )

        # variables for radio to select
        self.dimension_selected = tk.IntVar()

        self.radio_3d = ttk.Radiobutton(
            self.dimension_selector_frame,
            text="3D",
            variable=self.dimension_selected,
            value=self.SELECTED_3D,
            command=self.handle_switch_3d_plot
        )
        self.radio_3d.pack(
            side=tk.RIGHT,
            padx=10,
            pady=5
        )

        self.radio_2d = ttk.Radiobutton(
            self.dimension_selector_frame,
            text="2D",
            variable=self.dimension_selected,
            value=self.SELECTED_2D,
            command=self.handle_switch_2d_plot
        )
        self.radio_2d.pack(
            side=tk.LEFT,
            padx=10,
            pady=5
        )

    def handle_switch_3d_plot(self):
        self.recording.handle_switch_waterfall_plot()

    def handle_switch_2d_plot(self):
        self.recording.handle_switch_spec_plot()

    def disable_setting_pane(self):
        self.start_button["state"] = tk.DISABLED
        self.radio_2d.configure(state=tk.DISABLED)
        self.radio_3d.configure(state=tk.DISABLED)

    def enable_setting_pane(self):
        self.start_button["state"] = tk.NORMAL
        self.radio_2d.configure(state=tk.NORMAL)
        self.radio_3d.configure(state=tk.NORMAL)
