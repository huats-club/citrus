import tkinter as tk
from tkinter import filedialog as tkfd
from tkinter import ttk


class SavePane(ttk.Frame):
    def __init__(self, parent, controller, owner, side, pady=(20, 0), *args, **kwargs):

        self.parent = parent
        self.owner = owner
        self.controller = controller

        super().__init__(
            self.parent,
            relief=tk.GROOVE,
            *args,
            **kwargs
        )
        self.pack(
            side=side,  # TBC
            anchor=tk.CENTER,
            padx=10,
            pady=pady
        )

        # Label to prompt user to enter path to save to
        self.enter_save_path_label = ttk.Label(
            self,
            text="Enter path to save: "
        )
        self.enter_save_path_label.pack(
            side=tk.LEFT,
            padx=10,
            pady=5
        )

        # Filepath entry display
        self.filepath_text = tk.StringVar(value=self.controller.session.get_session_workspace_path())
        self.filepath_entry = ttk.Entry(
            self,
            width=50,
            textvariable=self.filepath_text,
            state="normal"
        )
        self.filepath_entry.pack(
            side=tk.LEFT,
            padx=10,
            pady=5
        )

        # Search button
        self.search_button = ttk.Button(
            self,
            style="primary.Outline.TButton",
            text="Search",
            command=self.get_filepath
        )
        self.search_button.pack(
            side=tk.LEFT,
            padx=10,
            pady=5
        )

        # Save button
        self.save_button = ttk.Button(
            self,
            style="primary.Outline.TButton",
            text="Save",
            command=self.owner.handle_save  # call interface common save method to be implmented by parent
        )
        self.save_button.pack(
            side=tk.RIGHT,
            padx=10,
            pady=5
        )

    def get_filepath(self):
        try:
            self.save_path = tkfd.askdirectory(initialdir="C:/")
            self.filepath_text.set(self.save_path)
            self.owner.update_save_path(self.save_path)
        except ValueError:
            self.filepath_text.set(self.controller.session.get_session_workspace_path())
