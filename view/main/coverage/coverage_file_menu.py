import tkinter as tk
from tkinter import filedialog as tkfd
from tkinter import ttk
from tkinter.constants import S


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
            width=70,
            textvariable=self.filepath_text,
            state="readonly"
        )
        self.filepath_entry.pack(
            side=tk.TOP
        )

        # Container to put buttons
        self.buttons_container = tk.Frame(
            self.container
        )
        self.buttons_container.pack(
            side=tk.BOTTOM
        )

        # Button to invoke dialog to select file to open
        self.filepath_entry_button = ttk.Button(
            self.buttons_container,
            style="primary.Outline.TButton",
            text="Select file",
            state="normal"
        )
        self.filepath_entry_button.pack(
            side=tk.LEFT,
            padx=10,
            pady=(5, 0)
        )

        # Upload dxf button
        self.upload_button = ttk.Button(
            self.buttons_container,
            style="primary.Outline.TButton",
            text="Open file",
            state="normal"
        )
        self.upload_button.pack(
            side=tk.LEFT,
            padx=10,
            pady=(5, 0)
        )

        # Clear dxf button
        self.clear_button = ttk.Button(
            self.buttons_container,
            style="primary.Outline.TButton",
            text="Clear file",
            state="normal"
        )
        self.clear_button.pack(
            side=tk.RIGHT,
            padx=10,
            pady=(5, 0)
        )

    def select_dxf_filepath(self):
        try:
            self.path = tkfd.askopenfilename(
                initialdir="C:/", filetypes=(("dxf files", "*.dxf"),
                                             ("all files", "*.*")))
            self.filepath_text.set(self.path)
        except ValueError:
            self.filepath_text.set("")

    def get_dxf_filepath_selected(self):
        return self.filepath_text.get(), self.filepath_text.get().split("/")[-1]
