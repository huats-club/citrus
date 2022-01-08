import tkinter as tk
from tkinter import filedialog as tkfd
from tkinter import ttk


class ReplaySettingPane(tk.Frame):
    def __init__(self, parent, replay, controller, *args, **kwargs):

        self.parent = parent
        self.controller = controller
        self.replay = replay

        self.SELECTED_2D = 1
        self.SELECTED_3D = 0

        super().__init__(self.parent, *args, **kwargs)
        self.pack(
            side=tk.BOTTOM,
            anchor=tk.CENTER
        )

        # Start button
        self.start_button = ttk.Button(
            self,
            style="primary.Outline.TButton",
            text="Start"
        )
        self.start_button.pack(
            side=tk.LEFT,
            padx=10,
            pady=10
        )

        # Toggle 2D / 3D view - radio buttons
        self.dimension_selector_frame = ttk.Frame(
            self,
            relief=tk.GROOVE
        )
        self.dimension_selector_frame.pack(
            side=tk.LEFT,
            padx=10,
            pady=10
        )

        # Create label to instruct users to select dimensions
        self.dimension_selector_label = ttk.Label(
            self.dimension_selector_frame,
            text="Select Plot: "
        )
        self.dimension_selector_label.pack(
            side=tk.LEFT,
            padx=10,
            pady=10
        )

        # variables for radio to select
        self.dimension_selected = tk.IntVar()

        # Create 3D radio button
        self.radio_3d = ttk.Radiobutton(
            self.dimension_selector_frame,
            text="3D Recording",
            variable=self.dimension_selected,
            value=self.SELECTED_3D
        )
        self.radio_3d.pack(
            side=tk.RIGHT,
            padx=10,
            pady=10
        )

        # Create 2D radio button
        self.radio_2d = ttk.Radiobutton(
            self.dimension_selector_frame,
            text="2D Recording",
            variable=self.dimension_selected,
            value=self.SELECTED_2D
        )
        self.radio_2d.pack(
            side=tk.RIGHT,
            padx=10,
            pady=10
        )

        # Create spectrum
        self.radio_spectrum = ttk.Radiobutton(
            self.dimension_selector_frame,
            text="Spectrum",
            variable=self.dimension_selected,
            value=self.SELECTED_2D
        )
        self.radio_spectrum.pack(
            side=tk.RIGHT,
            padx=10,
            pady=10
        )

        # Filepath
        self.file_path_frame = ttk.Frame(
            self,
            relief=tk.GROOVE
        )
        self.file_path_frame.pack(
            side=tk.LEFT,
            padx=10,
            pady=10
        )

        # Label to prompt user to search
        self.enter_save_path_label = ttk.Label(
            self.file_path_frame,
            text="Enter path to data: "
        )
        self.enter_save_path_label.pack(
            side=tk.LEFT,
            padx=10,
            pady=5
        )

        # Filepath entry display
        self.filepath_text = tk.StringVar(value="")
        self.filepath_entry = ttk.Entry(
            self.file_path_frame,
            width=100,
            textvariable=self.filepath_text,
            state="normal"
        )
        self.filepath_entry.pack(
            side=tk.LEFT,
            padx=10,
            pady=10
        )

        # Search button
        self.search_button = ttk.Button(
            self.file_path_frame,
            style="primary.Outline.TButton",
            text="Search",
            command=self.get_filepath
        )
        self.search_button.pack(
            side=tk.LEFT,
            padx=10,
            pady=10
        )

    def get_filepath(self):
        try:
            self.save_path = tkfd.askopenfilename(initialdir="C:/")
            self.filepath_text.set(self.save_path)
        except ValueError:
            self.filepath_text.set(self.controller.session.get_session_workspace_path())
