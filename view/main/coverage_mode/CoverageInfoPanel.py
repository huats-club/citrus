import tkinter as tk
from tkinter import ttk


class CoverageInfoPanel(tk.Frame):
    def __init__(self, parent, controller, *args, **kwargs):
        self.parent = parent
        self.controller = controller

        super().__init__(
            self.parent,
            *args, **kwargs
        )
        self.pack(
            padx=10,
            pady=10,
            side=tk.TOP,
            anchor=tk.NW,
            fill=tk.BOTH
        )

        # Message variable to store error message
        self.warning_text = tk.StringVar()

        self.message_label = ttk.Label(
            self,
            style="danger.TLabel",
            textvariable=self.warning_text
        )
        self.message_label.pack(
            side=tk.LEFT
        )

    def set_no_dxf_error_message(self):
        self.warning_text.set("Error! No dxf file selected.")
        self.after(5000, self.clear_error_message)

    def set_load_dxf_error_message(self):
        self.warning_text.set("Error! Dxf file cannot be loaded.")
        self.after(5000, self.clear_error_message)

    def clear_error_message(self):
        self.warning_text.set("")

    def set_no_wifi_scan_error_message(self):
        self.warning_text.set("Error! Select Wifi points on floorplan.")
        self.after(5000, self.clear_error_message)
