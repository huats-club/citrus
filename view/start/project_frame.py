import tkinter as tk
from tkinter import filedialog as tkfd
from tkinter import ttk

import config.app_parameters as app_parameters


class ProjectFrame(ttk.LabelFrame):
    def __init__(self, parent, *args, **kwargs):
        self.parent = parent

        # Create interface frame object
        super().__init__(
            self.parent,
            style="info.inverse.TLabelframe",
            text="Project Workspace",
            *args, **kwargs
        )
        self.pack(
            side=tk.TOP,
            padx=8,
            pady=8,
            fill=tk.BOTH,
            expand=True
        )

        # Create container to put inside interface frame
        self.project_frame_container = tk.Frame(self)
        self.project_frame_container.pack(
            anchor=tk.NW,
            padx=5,
            pady=5
        )

        # Create option for new or existing project
        self.selected = tk.StringVar()

        self.radio_new_project = ttk.Radiobutton(
            self.project_frame_container,
            text="New Project",
            value=app_parameters.PROJECT_NEW,
            variable=self.selected
        )
        self.radio_new_project.pack(
            fill="both",
            padx=5,
            pady=5
        )

        self.radio_load_project = ttk.Radiobutton(
            self.project_frame_container,
            text="Load Existing Project",
            value=app_parameters.PROJECT_LOAD,
            variable=self.selected
        )
        self.radio_load_project.pack(
            fill="both",
            padx=5,
            pady=5
        )

        # Container to store filepath choosing part
        self.filepath_container = tk.Frame(
            self.project_frame_container
        )
        self.filepath_container.pack()

        # Filepath entry display
        self.filepath_text = tk.StringVar()
        self.filepath_entry = ttk.Entry(
            self.filepath_container,
            width=50,
            textvariable=self.filepath_text,
            state="readonly"
        )
        self.filepath_entry.pack(
            padx=(25, 10),
            side=tk.LEFT
        )
        # Button to invoke dialog to select file to open
        self.filepath_entry_button = ttk.Button(
            self.filepath_container,
            style="primary.Outline.TButton",
            text="Select",
            state="disabled"
        )
        self.filepath_entry_button.pack(
            side=tk.RIGHT
        )

    def get_session_type_selection(self):
        return self.selected.get(), self.filepath_text.get()

    def enable_loading_config(self):
        self.filepath_entry_button.configure(state="normal")

    def disable_loading_config(self):
        self.filepath_entry_button.configure(state="disabled")
        self.filepath_text.set("")

    def get_filepath_from_radio_option(self):
        try:
            self.path = tkfd.askdirectory(initialdir="C:/")
            self.filepath_text.set(self.path)
        except ValueError:
            self.filepath_text.set("")
