import tkinter as tk
from tkinter import ttk


class CoverageValuesMenu(ttk.LabelFrame):
    def __init__(self, parent, controller, *args, **kwargs):
        self.parent = parent
        self.controller = controller

        super().__init__(
            self.parent,
            text="Strength Menu",
            *args, **kwargs
        )
        self.pack(
            padx=10,
            pady=10,
            side=tk.TOP,
            anchor=tk.NW,
            fill=tk.BOTH
        )

        # Create panel for input of sensitivity of rssi
        self.panel_container = ttk.Frame(self)
        self.panel_container.pack(
            padx=10,
            pady=(10, 5),
            side=tk.TOP,
            anchor=tk.NW,
            fill=tk.BOTH
        )

        # Max sensitivity
        self.max_sensitivity_label = tk.Label(
            self.panel_container,
            text="Max dBm",
            width=8,
            anchor=tk.NW
        )
        self.max_sensitivity_label.grid(
            row=0,
            column=0,
            columnspan=4,
            padx=5,
            pady=5
        )
        self.max_sensitivity_text = tk.StringVar()
        self.max_sensitivity = ttk.Entry(
            self.panel_container,
            textvariable=self.max_sensitivity_text
        )
        self.max_sensitivity.grid(
            row=0,
            column=5,
            columnspan=2,
            padx=5,
            pady=5
        )

        # Min sensitivity
        self.min_sensitivity_label = tk.Label(
            self.panel_container,
            text="Min dBm",
            width=8,
            anchor=tk.NW
        )
        self.min_sensitivity_label.grid(
            row=0,
            column=7,
            columnspan=4,
            padx=5,
            pady=5
        )
        self.min_sensitivity_text = tk.StringVar()
        self.min_sensitivity = ttk.Entry(
            self.panel_container,
            textvariable=self.min_sensitivity_text
        )
        self.min_sensitivity.grid(
            row=0,
            column=11,
            columnspan=2,
            padx=5,
            pady=5
        )

    def has_valid_dbm_settings(self):
        flag = True

        try:
            float(self.max_sensitivity_text.get())
            float(self.min_sensitivity_text.get())
        except ValueError:
            flag = False

        return flag

    def get_max_dbm(self):
        pass

    def get_min_dbm(self):
        pass
