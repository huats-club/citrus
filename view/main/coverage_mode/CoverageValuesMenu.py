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
            text="Max sensitivity",
            width=15,
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
            text="Min sensitivity",
            width=15,
            anchor=tk.NW
        )
        self.min_sensitivity_label.grid(
            row=1,
            column=0,
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
            row=1,
            column=5,
            columnspan=2,
            padx=5,
            pady=5
        )

        # Button Containers
        self.button_containers = tk.Frame(self)
        self.button_containers.pack(side=tk.BOTTOM)

        # TODO: fix the command
        # Configure rssi sensitivity button
        self.button = ttk.Button(
            self.button_containers,
            style="primary.Outline.TButton",
            text="Configure"
        )
        self.button.pack(
            padx=5,
            pady=(0, 10),
            side=tk.TOP,
            anchor=tk.CENTER
        )
