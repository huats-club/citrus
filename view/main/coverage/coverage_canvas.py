import tkinter as tk

import config.app_parameters as app_parameters
from PIL import ImageGrab
from view.canvas_tool_tip import CanvasTooltip


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
        self.bind("<Button-1>", lambda event: self.controller.on_coverage_put_point(event, self.coverage))

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

    def canvas_put_point(self, x, y, hovertext):
        python_green = "#476042"

        # Get points from button click
        x1, y1 = (x - 5), (y - 5)
        x2, y2 = (x + 5), (y + 5)

        # Display oval drawing
        oval_ui = self.create_oval(x1, y1, x2, y2, fill=python_green)
        CanvasTooltip(self, oval_ui, text=hovertext)

    def canvas_put_point_again(self, map_points):
        python_green = "#476042"

        for point in list(map_points.values()):
            # Get points from button click
            x1, y1 = (point.x - 5), (point.y - 5)
            x2, y2 = (point.x + 5), (point.y + 5)

            oval_ui = self.create_oval(x1, y1, x2, y2, fill=python_green)
            CanvasTooltip(self, oval_ui, text=point)

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
