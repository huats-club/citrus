import tkinter as tk
from tkinter import ttk


class CoverageMenu(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        self.parent = parent
        super().__init__(self.parent, *args, **kwargs)
        self.pack(
            side=tk.RIGHT
        )
