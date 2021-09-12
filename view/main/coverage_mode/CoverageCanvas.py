import tkinter as tk
from tkinter import ttk


class CoverageCanvas(tk.Canvas):
    def __init__(self, parent, controller, *args, **kwargs):
        self.parent = parent
        self.controller = controller

        super().__init__(self.parent,  *args, **kwargs)
        self.pack(
            padx=4,
            pady=4,
            fill=tk.BOTH,
            expand=True,  # ensures fill out the the parent
            side=tk.LEFT
        )
