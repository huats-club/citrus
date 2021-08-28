import tkinter as tk
from tkinter import filedialog as tkfd
from tkinter import ttk


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
            side=tk.BOTTOM,
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
            value="test2",
            variable=self.selected,
            command=self.disableLoadingConfig
        )
        self.radio_new_project.pack(
            fill="both",
            padx=5,
            pady=5
        )

        self.radio_load_project = ttk.Radiobutton(
            self.project_frame_container,
            text="Load Existing Project",
            value="test",
            variable=self.selected,
            command=self.enableLoadingConfig
        )
        self.radio_load_project.pack(
            fill="both",
            padx=5,
            pady=5
        )

        self.filepath_container = tk.Frame(
            self.project_frame_container
        )
        self.filepath_container.pack()

        # Filepath entry
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
        self.filepath_entry_button = ttk.Button(
            self.filepath_container,
            style="primary.Outline.TButton",
            text="Select file",
            state="disabled",
            command=self.getfile
        )
        self.filepath_entry_button.pack(
            side=tk.RIGHT
        )

    def getSelection(self):
        return self.selected.get()

    def enableLoadingConfig(self):
        self.filepath_entry_button.configure(state="normal")

    def disableLoadingConfig(self):
        self.filepath_entry_button.configure(state="disabled")

    def getfile(self):
        path = tkfd.askopenfile()
        self.filepath_text.set(path.name)
