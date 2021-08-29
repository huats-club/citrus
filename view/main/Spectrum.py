from tkinter import ttk


class SpectrumPage(ttk.Frame):
    def __init__(self, parent, controller, *args, **kwargs):
        self.parent = parent
        self.controller = controller
        super().__init__(self.parent,  *args, **kwargs)
