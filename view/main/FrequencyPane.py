import tkinter as tk
from tkinter import ttk

import AppParameters as app_params


class FrequencyPane(ttk.LabelFrame):
    def __init__(self, parent, controller, units_state=app_params.SPECTRUM_PLOT_UNITS_PREFIX_MEGA_X, *args, **kwargs):  # default state uses megahz
        self.parent = parent
        self.controller = controller

        # Current units state
        self.units_state = units_state

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

        self.units_text = tk.StringVar()
        self.units_text.set(units_state+app_params.SPECTRUM_PLOT_UNITS_POSTFIX_X)

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
            width=8,
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
        self.start_freq_units = ttk.Label(
            self.panel_container,
            width=5,
            textvariable=self.units_text
        )
        self.start_freq_units.grid(
            row=0,
            column=4,
            padx=5,
            pady=5
        )

        # Stop freq label
        self.stop_freq_label = tk.Label(
            self.panel_container,
            text="Stop",
            width=8,
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
        self.stop_freq_units = ttk.Label(
            self.panel_container,
            width=5,
            textvariable=self.units_text
        )
        self.stop_freq_units.grid(
            row=1,
            column=4,
            padx=5,
            pady=5
        )

        # Center freq label
        self.center_freq_label = tk.Label(
            self.panel_container,
            text="Center",
            width=8,
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
        self.center_freq_units = ttk.Label(
            self.panel_container,
            width=5,
            textvariable=self.units_text
        )
        self.center_freq_units.grid(
            row=2,
            column=4,
            padx=5,
            pady=5
        )

        # Button Containers
        self.button_containers = tk.Frame(self)
        self.button_containers.pack(side=tk.BOTTOM)

        # Submit button
        self.submit_button = ttk.Button(
            self.button_containers,
            style="primary.TButton",
            text="Configure"
        )
        self.submit_button.pack(
            padx=10,
            pady=10,
            side=tk.LEFT,
            anchor=tk.CENTER
        )

        # Toggle button
        self.toggle_button = ttk.Button(
            self.button_containers,
            style="primary.TButton",
            text="Toggle units",
            command=self.toggle_units
        )
        self.toggle_button.pack(
            padx=10,
            pady=10,
            side=tk.RIGHT,
            anchor=tk.CENTER
        )

    def toggle_units(self):

        # TODO: CONVERSION OF FREQ IN INPUT ENTRY

        if self.units_state == app_params.SPECTRUM_PLOT_UNITS_PREFIX_KILO_X:
            self.units_state = app_params.SPECTRUM_PLOT_UNITS_PREFIX_MEGA_X
            self.units_text.set(app_params.SPECTRUM_PLOT_UNITS_PREFIX_MEGA_X + app_params.SPECTRUM_PLOT_UNITS_POSTFIX_X)

        elif self.units_state == app_params.SPECTRUM_PLOT_UNITS_PREFIX_MEGA_X:
            self.units_state = app_params.SPECTRUM_PLOT_UNITS_PREFIX_GIGA_X
            self.units_text.set(app_params.SPECTRUM_PLOT_UNITS_PREFIX_GIGA_X + app_params.SPECTRUM_PLOT_UNITS_POSTFIX_X)

        elif self.units_state == app_params.SPECTRUM_PLOT_UNITS_PREFIX_GIGA_X:
            self.units_state = app_params.SPECTRUM_PLOT_UNITS_PREFIX_KILO_X
            self.units_text.set(app_params.SPECTRUM_PLOT_UNITS_PREFIX_KILO_X + app_params.SPECTRUM_PLOT_UNITS_POSTFIX_X)
