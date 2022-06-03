import tkinter as tk
from tkinter import ttk


class CoverageSdrTab(ttk.Frame):
    def __init__(self, parent, controller, coverage, *args, **kwargs):
        self.parent = parent
        self.controller = controller
        self.coverage = coverage

        super().__init__(
            self.parent,
            *args, **kwargs
        )
        self.pack(
            side=tk.BOTTOM,
            fill=tk.X
        )

        # String length for button
        self.STRING_LENGTH = 10

        # uuid for selected
        self.iid = 0

        # Create column name list to show tracked freq
        self.column_names = [
            'name',
            'freq (MHz)'
        ]

        self.column_width = {
            'name': 100,
            'freq (MHz)': 50
        }

        # Create main container
        self.container = ttk.Frame(self)
        self.container.pack(
            padx=4,
            pady=4,
            side=tk.TOP,
            anchor=tk.NW,
            fill=tk.BOTH,
            expand=True
        )

        # ---------------------------------------------

        # Create container for form to calibrate
        self.calibration_container = ttk.LabelFrame(self.container, text="Calibration")
        self.calibration_container.pack(
            padx=10,
            pady=10,
            side=tk.TOP,
            anchor=tk.NW,
            fill=tk.BOTH
        )

        self.calibration_internal_container = ttk.Frame(self.calibration_container)
        self.calibration_internal_container.pack(
            padx=10,
            pady=10,
            side=tk.TOP,
            anchor=tk.NW,
            fill=tk.BOTH
        )

        # Input tracked freq name label and entry box
        self.center_freq_calibration_label = tk.Label(
            self.calibration_internal_container,
            text="Center Frequency",
            width=15,
            anchor=tk.NW
        )
        self.center_freq_calibration_label.grid(
            row=0,
            column=0,
            columnspan=4,
            padx=5,
            pady=5
        )
        self.center_freq_calibration_text = tk.StringVar()
        self.center_freq_calibration = ttk.Entry(
            self.calibration_internal_container,
            textvariable=self.center_freq_calibration_text
        )
        self.center_freq_calibration.grid(
            row=0,
            column=5,
            columnspan=2,
            padx=5,
            pady=5
        )
       # TODO: toggle units?
        self.calibration_freq_units2 = ttk.Label(
            self.calibration_internal_container,
            width=5,
            text="MHz"
        )
        self.calibration_freq_units2.grid(
            row=0,
            column=7,
            columnspan=2,
            padx=5,
            pady=5
        )
        self.calibration_bandwidth_label = tk.Label(
            self.calibration_internal_container,
            text="Bandwidth",
            width=15,
            anchor=tk.NW
        )
        self.calibration_bandwidth_label.grid(
            row=1,
            column=0,
            columnspan=4,
            padx=5,
            pady=5
        )
        self.calibration_bandwidth_text = tk.StringVar()
        self.calibration_bandwidth = ttk.Entry(
            self.calibration_internal_container,
            textvariable=self.calibration_bandwidth_text
        )
        self.calibration_bandwidth.grid(
            row=1,
            column=5,
            columnspan=2,
            padx=5,
            pady=5
        )
        # TODO: toggle units?
        self.calibration_freq_units = ttk.Label(
            self.calibration_internal_container,
            width=5,
            text="MHz"
        )
        self.calibration_freq_units.grid(
            row=1,
            column=7,
            columnspan=2,
            padx=5,
            pady=5
        )
        self.calibration_button = ttk.Button(
            self.calibration_internal_container,
            style="success.TButton",
            text="Calibrate".center(self.STRING_LENGTH, ' '),
            command=lambda: self.controller.on_coverage_calibrate(self.coverage)
        )
        self.calibration_button.grid(
            row=0,
            column=9,
            # columnspan=4,
            padx=5,
            pady=5
        )

        self.error_message = tk.StringVar()
        self.error_message_label = ttk.Label(
            self.calibration_container,
            style="danger.TLabel",
            textvariable=self.error_message
        )
        self.error_message_label.pack(
            padx=10,
            pady=10,
            anchor=tk.CENTER
        )

        # -------------------------------------------------------

        # Label to inform display tracking
        self.tracking_label = ttk.Label(
            self.container,
            text="Tracking Frequencies:"
        )
        self.tracking_label.pack(
            side=tk.TOP,
            anchor=tk.NW,
            padx=10,
            pady=5
        )

        # Create display treeview panel to show all freq tracked
        self.tracking_panel = ttk.Treeview(
            self.container,
            show='headings',
            style='primary.Treeview',
            columns=self.column_names,
            height=5
        )
        self.tracking_panel.pack(
            padx=4,
            pady=4,
            fill=tk.BOTH,
            expand=True,
            anchor=tk.NW,
            side=tk.TOP
        )

        # Setup columns and headings
        for column_name in self.column_names:
            self.tracking_panel.column(
                column_name,
                width=self.column_width[column_name],
                anchor=tk.CENTER
            )
            self.tracking_panel.heading(
                column_name,
                text=column_name,
                anchor=tk.CENTER
            )

        # ---------------------------------------------

        # Create container for form to input tracked freq
        self.form_container = ttk.LabelFrame(self, text="Add New Frequency")
        self.form_container.pack(
            padx=10,
            pady=10,
            side=tk.TOP,
            anchor=tk.NW,
            fill=tk.BOTH
        )

        self.form_internal_container = ttk.Frame(self.form_container)
        self.form_internal_container.pack(
            padx=10,
            pady=10,
            side=tk.TOP,
            anchor=tk.NW,
            fill=tk.BOTH
        )

        # Input tracked freq name label and entry box
        self.tracked_name_label = tk.Label(
            self.form_internal_container,
            text="Name",
            width=15,
            anchor=tk.NW
        )
        self.tracked_name_label.grid(
            row=0,
            column=0,
            columnspan=4,
            padx=5,
            pady=5
        )
        self.tracked_name_text = tk.StringVar()
        self.tracked_name = ttk.Entry(
            self.form_internal_container,
            textvariable=self.tracked_name_text
        )
        self.tracked_name.grid(
            row=0,
            column=5,
            columnspan=2,
            padx=5,
            pady=5
        )

        # Input tracked freq label and entry box
        self.tracked_freq_label = tk.Label(
            self.form_internal_container,
            text="Tracked Frequency",
            width=15,
            anchor=tk.NW
        )
        self.tracked_freq_label.grid(
            row=1,
            column=0,
            columnspan=4,
            padx=5,
            pady=5
        )
        self.tracked_freq_text = tk.StringVar()
        self.tracked_freq = ttk.Entry(
            self.form_internal_container,
            textvariable=self.tracked_freq_text
        )
        self.tracked_freq.grid(
            row=1,
            column=5,
            columnspan=2,
            padx=5,
            pady=5
        )
        # TODO: toggle units?
        self.freq_units = ttk.Label(
            self.form_internal_container,
            width=5,
            text="MHz"
        )
        self.freq_units.grid(
            row=1,
            column=7,
            columnspan=2,
            padx=5,
            pady=5
        )

        # Button Containers
        self.button_containers = tk.Frame(self)
        self.button_containers.pack(side=tk.TOP)

        self.track_button = ttk.Button(
            self.button_containers,
            style="success.TButton",
            text="Track".center(self.STRING_LENGTH, ' '),
            command=lambda: self.move_item_to_selected()
        )
        self.track_button.pack(
            padx=5,
            pady=(0, 10),
            side=tk.LEFT,
            anchor=tk.CENTER
        )

        self.untrack_button = ttk.Button(
            self.button_containers,
            style="secondary.TButton",
            text="Untrack".center(self.STRING_LENGTH, ' '),
            command=lambda: self.remove_item_from_selected()
        )
        self.untrack_button.pack(
            padx=5,
            pady=(0, 10),
            side=tk.LEFT,
            anchor=tk.CENTER
        )

        self.clear_button = ttk.Button(
            self.button_containers,
            style="danger.TButton",
            text="Clear".center(self.STRING_LENGTH, ' '),
            command=lambda: self.clear_all_sdr_panel()
        )
        self.clear_button.pack(
            padx=5,
            pady=(0, 10),
            side=tk.LEFT,
            anchor=tk.CENTER
        )

    def select_item(self, a):
        self.current_selected_focus = self.tracking_panel.focus()

    def get_bandwidth(self):
        try:
            bandwidth = float(self.calibration_bandwidth_text.get()) * 1e6
            print(f"bandwidth: {bandwidth}")
        except ValueError:
            return ""
        return bandwidth

    def get_center_freq(self):
        try:
            center_freq = float(self.center_freq_calibration_text.get()) * 1e6
        except ValueError:
            return ""
        return center_freq

    def disable_calibration_button(self):
        self.calibration_button.configure(state="disabled")

    def enable_calibration_button(self):
        self.calibration_button.configure(state="normal")

    # TODO: maybe abstract into another message container/class later
    def display_calibration_message(self):
        self.error_message.set("Calibration in progress.")

    def display_calibration_done(self):
        self.clear_error_message()
        self.error_message.set("Calibration done.")
        self.after(3000, self.clear_error_message)

    # TODO: maybe abstract into another message container/class later
    def display_calibration_error_message(self):
        self.error_message.set("Error! Calibration not done.")
        self.after(3000, self.clear_error_message)

    # TODO: maybe abstract into another message container/class later
    def clear_error_message(self):
        self.error_message.set("")

    # Move the selected item in the Display ALL panel to selected panel
    def move_item_to_selected(self):
        data = (self.tracked_name_text.get(), self.tracked_freq_text.get())
        self.tracked_name_text.set("")
        self.tracked_freq_text.set("")
        self.tracking_panel.insert(parent='', index=self.iid, iid=self.iid, values=data)
        self.iid += 1

    def remove_item_from_selected(self):
        # If no items clicked, ignore
        if not self.tracking_panel.focus():
            return

        self.tracking_panel.delete(self.tracking_panel.focus())

    def clear_all_sdr_panel(self):
        self.tracking_panel.delete(*self.tracking_panel.get_children())

    # Get dict of tracked (name->freq)
    # so that the sdr can run scan/extract check against this list
    def get_tracked_map_name_freq(self):

        tracked = []
        temp_keys = []

        for child in self.tracking_panel.get_children():
            all_data = self.tracking_panel.item(child)["values"]

            name = all_data[0]
            try:
                freq = float(all_data[1]) * 1e6  # convert to mhz
            except ValueError:
                continue

            # print(name, freq)

            # temp
            temp = {}

            temp[name] = freq

            # record
            temp_keys.append(name)

            # append
            tracked.append(temp)

        return tracked
