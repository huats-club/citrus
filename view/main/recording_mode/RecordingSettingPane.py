import tkinter as tk
from tkinter import ttk


class RecordingSettingPane(tk.Frame):
    def __init__(self, parent, recording, controller, *args, **kwargs):

        self.parent = parent
        self.controller = controller
        self.recording = recording

        super().__init__(self.parent, *args, **kwargs)
        self.pack(
            side=tk.BOTTOM
        )

        # Start button
        self.start_button = ttk.Button(
            self,
            style="primary.TButton",
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
            style="primary.TButton",
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
            style="primary.TButton",
            text="Save",
            command=self.recording.handle_recording_save
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
