import tkinter as tk
from tkinter import filedialog as tkfd
from tkinter import ttk


class CoverageFileMenu(ttk.LabelFrame):
    def __init__(self, parent, controller, *args, **kwargs):
        self.parent = parent
        self.controller = controller

        super().__init__(
            self.parent,
            text="File Menu",
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
        self.container = ttk.Frame(self)
        self.container.pack(
            padx=10,
            pady=10,
            side=tk.TOP,
            anchor=tk.NW,
            fill=tk.BOTH
        )

        # Create option for file to open
        self.selected_dxf = tk.StringVar()

        # Container to store filepath choosing part
        self.filepath_container = tk.Frame(
            self.container
        )
        self.filepath_container.pack()

        # Filepath entry display
        self.filepath_text = tk.StringVar()
        self.filepath_entry = ttk.Entry(
            self.filepath_container,
            width=30,
            textvariable=self.filepath_text,
            state="readonly"
        )
        self.filepath_entry.pack(
            side=tk.LEFT
        )
        # Button to invoke dialog to select file to open
        self.filepath_entry_button = ttk.Button(
            self.filepath_container,
            style="primary.Outline.TButton",
            text="Select file",
            state="normal",
            command=self.get_dxf_filepath
        )
        self.filepath_entry_button.pack(
            side=tk.RIGHT
        )

    def get_dxf_filepath(self):
        try:
            self.path = tkfd.askopenfilename(
                initialdir="C:/", filetypes=(("dxf files", "*.dxf"),
                                             ("all files", "*.*")))
            self.filepath_text.set(self.path)
        except ValueError:
            self.filepath_text.set("")
