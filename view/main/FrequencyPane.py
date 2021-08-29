import tkinter as tk
from tkinter import ttk


class FrequencyPane(ttk.LabelFrame):
    def __init__(self, parent, controller, *args, **kwargs):
        self.parent = parent
        self.controller = controller

        super().__init__(
            self.parent,
            text="Frequency Panel",
            *args, **kwargs
        )
        self.pack(
            padx=10,
            pady=10,
            side=tk.TOP,
            anchor=tk.NW,
            fill=tk.BOTH
        )

        # Create panel for input of start/stop freq
        self.panel_container = ttk.Frame(self)
        self.panel_container.pack(
            padx=10,
            pady=(10, 5),
            side=tk.TOP,
            anchor=tk.NW,
            fill=tk.BOTH
        )

        # Start freq label
        self.start_freq_label = tk.Label(
            self.panel_container,
            text="Start",
            width=10,
            anchor=tk.NW
        )
        self.start_freq_label.grid(
            row=0,
            column=0,
            columnspan=2,
            padx=5,
            pady=5
        )
        self.start_freq_text = tk.StringVar()
        self.start_entry = ttk.Entry(
            self.panel_container,
            textvariable=self.start_freq_text
        )
        self.start_entry.grid(
            row=0,
            column=2,
            columnspan=2,
            padx=5,
            pady=5
        )

        # Stop freq label
        self.stop_freq_label = tk.Label(
            self.panel_container,
            text="Stop",
            width=10,
            anchor=tk.NW
        )
        self.stop_freq_label.grid(
            row=1,
            column=0,
            columnspan=2,
            padx=5,
            pady=5
        )
        self.stop_freq_text = tk.StringVar()
        self.stop_entry = ttk.Entry(
            self.panel_container,
            textvariable=self.stop_freq_text
        )
        self.stop_entry.grid(
            row=1,
            column=2,
            columnspan=2,
            padx=5,
            pady=5
        )

        # Center freq label
        self.center_freq_label = tk.Label(
            self.panel_container,
            text="Center",
            width=10,
            anchor=tk.NW
        )
        self.center_freq_label.grid(
            row=2,
            column=0,
            columnspan=2,
            padx=5,
            pady=5
        )
        self.center_freq_text = tk.StringVar()
        self.center_entry = ttk.Entry(
            self.panel_container,
            textvariable=self.center_freq_text,
            state=tk.DISABLED
        )
        self.center_entry.grid(
            row=2,
            column=2,
            columnspan=2,
            padx=5,
            pady=5
        )

        # Submit button
        self.button = ttk.Button(
            self,
            style="primary.TButton",
            text="Configure"
        )
        self.button.pack(
            padx=10,
            pady=10,
            side=tk.BOTTOM,
            anchor=tk.CENTER
        )
