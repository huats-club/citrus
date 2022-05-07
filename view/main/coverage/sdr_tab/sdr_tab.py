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

        # Currently selected row of data from list of tracked freq
        # map (col_name->val)
        self.current_selected = {}

        # for clearing purposes
        self.current_selected_focus = ""

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
            self.calibration_container,
            style="success.TButton",
            text="Calibrate".center(self.STRING_LENGTH, ' ')
        )
        self.calibration_button.pack(
            padx=5,
            pady=(0, 10),
            side=tk.BOTTOM,
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

        # # Allow clicking of treeview items
        # self.tracking_panel.bind('<ButtonRelease-1>', self.select_item)

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
            text="Track".center(self.STRING_LENGTH, ' ')
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
            text="Untrack".center(self.STRING_LENGTH, ' ')
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
            text="Clear".center(self.STRING_LENGTH, ' ')
        )
        self.clear_button.pack(
            padx=5,
            pady=(0, 10),
            side=tk.LEFT,
            anchor=tk.CENTER
        )
