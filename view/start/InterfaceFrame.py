import tkinter as tk
from tkinter import ttk

from app_parameters import app_parameters


class InterfaceFrame(ttk.LabelFrame):
    def __init__(self, parent, *args, **kwargs):
        self.parent = parent

        # Create interface frame object
        super().__init__(
            self.parent,
            style="info.inverse.TLabelframe",
            text="Select Interface",
            *args, **kwargs
        )
        self.pack(
            side=tk.TOP,
            anchor=tk.NW,
            padx=8,
            pady=8,
            fill=tk.BOTH,
            expand=True
        )

        # Create container to put inside interface frame
        self.interface_frame_container = tk.Frame(self)
        self.interface_frame_container.pack(
            padx=5,
            pady=5
        )

        # Create text instructions above dropdown
        self.interface_label = ttk.Label(
            self.interface_frame_container,
            text="Select an interface option:"
        )
        self.interface_label.pack(
            side=tk.TOP,
            padx=5,
            pady=5
        )

        # Create dropdown menu to select interface type
        self.interface_dropdown_selection = tk.StringVar()
        self.interface_dropdown = ttk.Combobox(
            self.interface_frame_container,
            state="readonly",
            textvariable=self.interface_dropdown_selection
        )
        self.interface_dropdown.pack(
            side=tk.BOTTOM,
            padx=5,
            pady=5
        )

        # List of interfaces available for selection
        self.interface_dropdown['values'] = app_parameters.INTERFACE_LIST

    def getInterfaceSelected(self):
        return self.interface_dropdown_selection.get()
