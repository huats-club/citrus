import tkinter as tk
from tkinter import ttk


class SelectDriverPane(ttk.LabelFrame):
    def __init__(self, parent, controller, *args, **kwargs):
        self.parent = parent
        self.controller = controller

        super().__init__(
            self.parent,
            text="Select Driver",
            *args, **kwargs
        )
        self.pack(
            padx=10,
            pady=10,
            side=tk.TOP,
            anchor=tk.NW,
            fill=tk.BOTH
        )

        # Create panel for input of selected driver
        self.panel_container = ttk.Frame(self)
        self.panel_container.pack(
            padx=10,
            pady=(10, 5),
            side=tk.TOP,
            anchor=tk.NW,
            fill=tk.BOTH
        )

        # Driver label
        self.select_driver_label = tk.Label(
            self.panel_container,
            text="Input driver",
            width=15,
            anchor=tk.NW
        )
        self.select_driver_label.grid(
            row=0,
            column=0,
            columnspan=4,
            padx=5,
            pady=5
        )
        self.select_driver_text = tk.StringVar()
        self.select_driver_text.set("lime")  # set default
        self.select_driver = ttk.Entry(
            self.panel_container,
            textvariable=self.select_driver_text
        )
        self.select_driver.grid(
            row=0,
            column=5,
            columnspan=2,
            padx=5,
            pady=5
        )

    # Returns the driver input entered
    def get_driver_input(self):
        return self.select_driver_text.get()
