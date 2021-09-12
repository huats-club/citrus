import tkinter as tk
from tkinter import ttk


class CoverageBar(ttk.Frame):
    def __init__(self, parent, controller, * args, **kwargs):
        self.parent = parent

        super().__init__(
            self.parent,
            *args, **kwargs
        )
        self.pack(
            padx=10,
            pady=10,
            side=tk.BOTTOM,
            anchor=tk.NW,
            fill=tk.BOTH
        )

        # Create container
        self.container = ttk.Frame(self)
        self.container.pack(
            padx=10,
            pady=(10, 5),
            side=tk.TOP,
            anchor=tk.NW,
            fill=tk.BOTH
        )
