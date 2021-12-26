import tkinter as tk

from app_parameters import app_parameters
from PIL import ImageGrab
from view.CanvasTooltip import CanvasTooltip


class CoverageCanvas(tk.Canvas):
    def __init__(self, parent, controller, coverage, *args, **kwargs):
        self.parent = parent
        self.controller = controller
        self.coverage = coverage

        super().__init__(self.parent,
                         width=app_parameters.CANVAS_WIDTH,
                         height=app_parameters.CANVAS_HEIGHT,
                         *args, **kwargs)
        self.pack(
            padx=4,
            pady=4,
            side=tk.TOP
        )

    def enable_click(self):
        # Bind button click to out point
        self.bind("<Button-1>", self.canvas_put_point)

    def disable_click(self):
        self.unbind("<Button-1>")

    def draw_arc(self, start_x, start_y, end_x, end_y, start_angle, extent):
        self.create_arc(start_x,
                        start_y,
                        end_x,
                        end_y,
                        start=start_angle,
                        extent=extent,
                        style="arc"
                        )

    def draw_line(self, start_x, start_y, end_x, end_y):
        self.create_line(start_x,
                         start_y,
                         end_x,
                         end_y
                         )

    def canvas_put_point(self, event):
        python_green = "#476042"

        # Get points from button click
        x1, y1 = (event.x - 5), (event.y - 5)
        x2, y2 = (event.x + 5), (event.y + 5)

        # Record point and associated signal
        # Returns created Point object
        point = self.coverage.add_point_data(event.x, event.y)

        # If no wifi tracked
        if point == None:
            return

        # Display oval drawing
        oval_ui = self.create_oval(x1, y1, x2, y2, fill=python_green)
        CanvasTooltip(self, oval_ui, text=point)

        # Set that new wifi heatmap needs to be regenerated
        self.controller.session.set_need_to_save()

    # Create image to save canvas to
    # Reason: wifi heatmap plotter needed this to etch the heatmap onto it
    def capture(self, path=""):

        # if no path supplied, means save to a default image path
        if path == "":
            self.controller.get_floorplan_image_path()

        box = (
            self.winfo_rootx(),
            self.winfo_rooty(),
            self.winfo_rootx() + self.winfo_width(),
            self.winfo_rooty() + self.winfo_height()
        )
        grab = ImageGrab.grab(bbox=box)
        grab.save(path)
