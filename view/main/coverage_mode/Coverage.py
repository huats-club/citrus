
import tkinter as tk
from tkinter import ttk

from app_parameters import app_parameters
from view.main.coverage_mode.CoverageBar import CoverageBar
from view.main.coverage_mode.CoverageCanvas import CoverageCanvas
from view.main.coverage_mode.CoverageFileMenu import CoverageFileMenu
from view.main.coverage_mode.CoverageMenu import CoverageMenu
from view.main.coverage_mode.CoverageValuesMenu import CoverageValuesMenu


class CoveragePage(ttk.Frame):
    def __init__(self, parent, controller, *args, **kwargs):
        self.parent = parent
        self.controller = controller

        super().__init__(self.parent,  *args, **kwargs)
        self.pack(
            padx=10,
            pady=10,
            fill=tk.BOTH,
            expand=True  # ensures fill out the the parent
        )

        # Create main container
        self.container = ttk.Frame(self)
        self.container.pack(
            padx=4,
            pady=4,
            fill=tk.BOTH,
            expand=True
        )

        # Create top half of container
        self.left_container = ttk.Frame(self.container)
        self.left_container.pack(
            padx=4,
            pady=4,
            fill=tk.BOTH,
            expand=True,
            side=tk.LEFT
        )

        # Create (menu) bottom half of container
        self.right_container = tk.Frame(self.container)
        self.right_container.pack(
            padx=4,
            pady=4,
            side=tk.RIGHT,
            fill=tk.BOTH
        )

        # Create canvas for left top container
        self.coverage_canvas = CoverageCanvas(self.left_container, self.controller)

        # Create bottom bar
        self.coverage_bar = CoverageBar(self.left_container, self.controller)

        # Create coverage menu to upload file
        self.coverage_file_menu = CoverageFileMenu(self.right_container, self.controller)

        # Create coverage menu bar for right top container
        self.coverage_menu = CoverageMenu(self.right_container, self.controller)

        # Create coverage value menu for right top container
        self.coverage_value_menu = CoverageValuesMenu(self.right_container, self.controller)

    def display_dxf(self, dxf):

        def print_entity(e):
            # print("LINE on layer: %s\n" % e.dxf.layer)
            # print("start point: %s\n" % e.dxf.start)
            # print("end point: %s\n" % e.dxf.end)
            print(f"Start: {e.dxf.start} | End: {e.dxf.end}")

        def print_entity_arc(e):
            # print("LINE on layer: %s\n" % e.dxf.layer)
            # print("start point: %s\n" % e.dxf.start)
            # print("end point: %s\n" % e.dxf.end)
            print(
                f"center: {e.dxf.center} | radius: {e.dxf.radius} | start angle: {e.dxf.start_angle} | end angle: {e.dxf.end_angle}")

        self.my_x = set()
        self.my_y = set()
        self.lines = []
        self.arcs = []

        # try to parse and make sense of dxf
        msp = dxf.modelspace()
        for e in msp:

            temp = {}

            if e.dxftype() == 'LINE':
                self.my_x.add(e.dxf.start[0])
                self.my_x.add(e.dxf.end[0])
                self.my_y.add(e.dxf.start[1])
                self.my_y.add(e.dxf.end[1])

                self.lines.append([e.dxf.start[0], e.dxf.start[1], e.dxf.end[0], e.dxf.end[1]])

            if e.dxftype() == 'ARC':
                center_x = e.dxf.center[0]
                center_y = e.dxf.center[1]
                radius = e.dxf.radius
                start_angle = e.dxf.start_angle
                end_angle = e.dxf.end_angle

                self.my_x.add(center_x)
                self.my_y.add(center_y)

                temp['center_x'] = center_x
                temp['center_y'] = center_y
                temp['radius'] = radius
                temp['start_angle'] = start_angle
                temp['end_angle'] = end_angle
                self.arcs.append(temp)

        sorted_x = sorted(list(self.my_x))
        sorted_y = sorted(list(self.my_y))

        x_bound = sorted_x[-1] + sorted_x[0]
        y_bound = sorted_y[-1] + sorted_y[0]

        for line in self.lines:
            line[0] = line[0] / x_bound * app_parameters.CANVAS_WIDTH
            line[2] = line[2] / x_bound * app_parameters.CANVAS_WIDTH

            line[1] = line[1] / y_bound * app_parameters.CANVAS_HEIGHT
            line[3] = line[3] / y_bound * app_parameters.CANVAS_HEIGHT

            self.coverage_canvas.draw_line(
                line[0],
                app_parameters.CANVAS_HEIGHT - line[1],
                line[2],
                app_parameters.CANVAS_HEIGHT - line[3]
            )

        for arc in self.arcs:
            start_x_left_upper = (arc['center_x'] - arc['radius']) / x_bound * app_parameters.CANVAS_WIDTH
            start_y_left_upper = (arc['center_y'] - arc['radius']) / y_bound * app_parameters.CANVAS_HEIGHT

            end_x_right_lower = (arc['center_x'] + arc['radius']) / x_bound * app_parameters.CANVAS_WIDTH
            end_y_right_lower = (arc['center_y'] + arc['radius']) / y_bound * app_parameters.CANVAS_HEIGHT

            self.coverage_canvas.draw_arc(
                start_x_left_upper,
                app_parameters.CANVAS_HEIGHT - start_y_left_upper,
                end_x_right_lower,
                app_parameters.CANVAS_HEIGHT - end_y_right_lower,
                arc['start_angle'],
                360 - (arc['start_angle'] - arc['end_angle'])
            )
