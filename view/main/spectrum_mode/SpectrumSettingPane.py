import tkinter as tk
from tkinter import ttk

from view.main.SavePane import SavePane


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
            style="primary.Outline.TButton",
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
            style="primary.Outline.TButton",
            text="Stop",
            command=self.spectrum.handle_spectrum_stop
        )
        self.stop_button.pack(
            side=tk.LEFT,
            padx=10,
            pady=(20, 0)
        )

        # Save button
        self.save_pane = SavePane(
            self,
            self.controller,
            self.spectrum,
            tk.RIGHT
        )
