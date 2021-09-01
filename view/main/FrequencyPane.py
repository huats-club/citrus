import tkinter as tk
from tkinter import ttk

import AppParameters as app_params


class FrequencyPane(ttk.LabelFrame):
    def __init__(self, parent, controller,
                 units_state=app_params.SPECTRUM_PLOT_UNITS_PREFIX_MEGA_X,
                 *args, **kwargs):  # default state uses megahz
        self.parent = parent
        self.controller = controller

        # Current units state
        self.units_state = units_state
        self.units_text = tk.StringVar()
        self.units_text.set(units_state+app_params.SPECTRUM_PLOT_UNITS_POSTFIX_X)

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
            side=tk.TOP,
            anchor=tk.CENTER
        )

        self.error_message = tk.StringVar()
        self.error_message_label = ttk.Label(
            self.parent,
            style="danger.TLabel",
            textvariable=self.error_message
        )
        self.error_message_label.pack(
            padx=10,
            pady=10,
            anchor=tk.CENTER
        )

        # Event to auto poll and populate center freq
        self.after(100, self.populate_center_freq)

    def disable_frequency_pane(self):
        # Only disable if is valid
        if self.is_start_stop_freq_valid():
            self.toggle_button["state"] = tk.DISABLED
            self.start_entry["state"] = tk.DISABLED
            self.stop_entry["state"] = tk.DISABLED

    def enable_frequency_pane(self):
        self.toggle_button["state"] = tk.NORMAL
        self.start_entry["state"] = tk.NORMAL
        self.stop_entry["state"] = tk.NORMAL

    def displayErrorMessage(self):
        self.error_message.set("Error! Check frequency before start.")
        self.after(3000, self.clearErrorMessage)

    def clearErrorMessage(self):
        self.error_message.set("")

    def toggle_units(self):

        if not self.is_start_stop_freq_valid():
            # print('not valid')
            return

        if self.units_state == app_params.SPECTRUM_PLOT_UNITS_PREFIX_KILO_X:
            self.units_state = app_params.SPECTRUM_PLOT_UNITS_PREFIX_MEGA_X
            self.units_text.set(app_params.SPECTRUM_PLOT_UNITS_PREFIX_MEGA_X + app_params.SPECTRUM_PLOT_UNITS_POSTFIX_X)

            self.start_freq_text.set(float(self.start_freq_text.get()) / (10**3))
            self.stop_freq_text.set(float(self.stop_freq_text.get()) / (10**3))
            self.center_freq_text.set(float(self.center_freq_text.get()) / (10**3))

        elif self.units_state == app_params.SPECTRUM_PLOT_UNITS_PREFIX_MEGA_X:
            self.units_state = app_params.SPECTRUM_PLOT_UNITS_PREFIX_GIGA_X
            self.units_text.set(app_params.SPECTRUM_PLOT_UNITS_PREFIX_GIGA_X + app_params.SPECTRUM_PLOT_UNITS_POSTFIX_X)

            self.start_freq_text.set(float(self.start_freq_text.get()) / (10**3))
            self.stop_freq_text.set(float(self.stop_freq_text.get()) / (10**3))
            self.center_freq_text.set(float(self.center_freq_text.get()) / (10**3))

        elif self.units_state == app_params.SPECTRUM_PLOT_UNITS_PREFIX_GIGA_X:
            self.units_state = app_params.SPECTRUM_PLOT_UNITS_PREFIX_KILO_X
            self.units_text.set(app_params.SPECTRUM_PLOT_UNITS_PREFIX_KILO_X + app_params.SPECTRUM_PLOT_UNITS_POSTFIX_X)

            self.start_freq_text.set(float(self.start_freq_text.get()) * 10**6)
            self.stop_freq_text.set(float(self.stop_freq_text.get()) * 10**6)
            self.center_freq_text.set(float(self.center_freq_text.get()) * 10**6)

    def get_freq_units(self):
        return self.units_state

    def get_start_freq(self):
        return self.start_freq_text.get()

    def get_stop_freq(self):
        return self.stop_freq_text.get()

    def get_center_freq(self):

        if self.units_state == app_params.SPECTRUM_PLOT_UNITS_PREFIX_GIGA_X:
            mag = 10 ** 9
        elif self.units_state == app_params.SPECTRUM_PLOT_UNITS_PREFIX_KILO_X:
            mag = 10 ** 3
        elif self.units_state == app_params.SPECTRUM_PLOT_UNITS_PREFIX_MEGA_X:
            mag = 10 ** 6

        return float(self.center_freq_text.get()) * mag

    def populate_center_freq(self):
        self.after(100, self.populate_center_freq)
        if self.is_start_stop_freq_valid():
            self.center_freq_text.set((float(self.start_freq_text.get()) + float(self.stop_freq_text.get()))/2)

    def is_start_stop_freq_valid(self):
        if self.start_freq_text.get().isnumeric() and self.stop_freq_text.get().isnumeric():
            return True
        else:
            # test for float
            try:
                float(self.start_freq_text.get())
                float(self.stop_freq_text.get())
            except ValueError:
                return False

            return True
