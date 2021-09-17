import tkinter as tk

from app_parameters import app_parameters


class CoverageCanvas(tk.Canvas):
    def __init__(self, parent, controller, *args, **kwargs):
        self.parent = parent
        self.controller = controller

        super().__init__(self.parent,
                         width=app_parameters.CANVAS_WIDTH,
                         height=app_parameters.CANVAS_HEIGHT,
                         *args, **kwargs)
        self.pack(
            padx=4,
            pady=4,
            fill=tk.BOTH,
            expand=True,  # ensures fill out the the parent
            side=tk.TOP
        )

        # self.bind("<MouseWheel>", self.do_zoom)
        # self.bind('<ButtonPress-1>', lambda event: self.scan_mark(event.x, event.y))
        # self.bind("<B1-Motion>", lambda event: self.scan_dragto(event.x, event.y, gain=1))

        # Create event to put points on canvas
        # self.bind("<Button-1>", self.canvas_put_point)

    def draw_arc(self, start_x, start_y, end_x, end_y, start_angle, extent):
        self.create_arc(start_x, start_y, end_x, end_y, start=start_angle, extent=extent, style="arc")

    def draw_line(self, start_x, start_y, end_x, end_y):
        self.create_line(start_x, start_y, end_x, end_y)

    def canvas_put_point(self, event):
        python_green = "#476042"

        # Get points from button click
        x1, y1 = (event.x - 2), (event.y - 2)
        x2, y2 = (event.x + 2), (event.y + 2)

        # Display oval drawing
        self.create_oval(x1, y1, x2, y2, fill=python_green)
