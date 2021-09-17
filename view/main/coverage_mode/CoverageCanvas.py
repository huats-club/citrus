import tkinter as tk


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
            side=tk.TOP
        )

        self.bind("<MouseWheel>", self.do_zoom)
        self.bind('<ButtonPress-1>', lambda event: self.scan_mark(event.x, event.y))
        self.bind("<B1-Motion>", lambda event: self.scan_dragto(event.x, event.y, gain=1))

    def draw_line(self, start_x, start_y, end_x, end_y):
        self.create_line(start_x, start_y, end_x, end_y)

    def do_zoom(self, event):
        x = self.canvasx(event.x)
        y = self.canvasy(event.y)
        factor = 1.001 ** event.delta
        self.scale(tk.ALL, x, y, factor, factor)
