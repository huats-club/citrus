from app_parameters import app_parameters


class dxf2tk:
    def __init__(self, coverage):
        self.coverage = coverage
        self.x_list = set()
        self.y_list = set()
        self.lines = []
        self.arcs = []

    def add_x(self, x):
        self.x_list.add(x)

    def add_y(self, y):
        self.y_list.add(y)

    def add_line(self, start_x, start_y, end_x, end_y):
        self.lines.append(
            {
                "start_x": start_x,
                "start_y": start_y,
                "end_x": end_x,
                "end_y": end_y
            }
        )

        self.add_x(start_x)
        self.add_x(end_x)
        self.add_y(start_y)
        self.add_y(end_y)

    def add_arc(self,
                center_x,
                center_y,
                radius,
                start_angle,
                end_angle
                ):
        self.arcs.append(
            {
                "center_x": center_x,
                "center_y": center_y,
                "radius": radius,
                "start_angle": start_angle,
                "end_angle": end_angle
            }
        )

        self.add_x(center_x)
        self.add_y(center_y)

    def dxf2tk_convert_y(self, y):
        return y / self.y_bound * app_parameters.CANVAS_HEIGHT

    def dxf2tk_convert_x(self, x):
        return x / self.x_bound * app_parameters.CANVAS_WIDTH

    def dxf2tk_vertical_flip(self, y):
        return app_parameters.CANVAS_HEIGHT - y

    def convert(self):
        self.sorted_x_list = sorted(list(self.x_list))
        self.sorted_y_list = sorted(list(self.y_list))

        self.x_min = self.sorted_x_list[0]
        self.y_min = self.sorted_y_list[0]
        self.x_max = self.sorted_x_list[-1]
        self.y_max = self.sorted_y_list[-1]

        # Maximum bound of dxf values
        self.x_bound = self.x_min + self.x_max
        self.y_bound = self.y_min + self.y_max

        # Save bounds in controller also
        self.coverage.x_bound = self.x_bound
        self.coverage.y_bound = self.y_bound

        # Store all lines / arcs in list of dictionary
        self.converted_lines = []
        self.converted_arcs = []

        # Convert all lines from dxf coordinates to tkinter coordinates
        for line in self.lines:
            # convert to tkinter
            converted_start_x = self.dxf2tk_convert_x(line["start_x"])
            converted_start_y = self.dxf2tk_convert_y(line["start_y"])

            converted_end_x = self.dxf2tk_convert_x(line["end_x"])
            converted_end_y = self.dxf2tk_convert_y(line["end_y"])

            # do vertical flip
            converted_start_y = self.dxf2tk_vertical_flip(converted_start_y)
            converted_end_y = self.dxf2tk_vertical_flip(converted_end_y)

            # Save in converted lines list
            self.converted_lines.append(
                {
                    "start_x": converted_start_x,
                    "start_y": converted_start_y,
                    "end_x": converted_end_x,
                    "end_y": converted_end_y
                }
            )

        # Convert all arc from dxf coordinates to tkinter coordinates
        for arc in self.arcs:
            # Compute rectangle corner edge coordinates
            x_left_upper = arc['center_x'] - arc['radius']
            y_left_upper = arc['center_y'] - arc['radius']

            x_right_lower = arc['center_x'] + arc['radius']
            y_right_lower = arc['center_y'] + arc['radius']

            # Convert arc coordinates to dxf
            converted_x_left_upper = self.dxf2tk_convert_x(x_left_upper)
            converted_y_left_upper = self.dxf2tk_convert_y(y_left_upper)

            converted_x_right_lower = self.dxf2tk_convert_x(x_right_lower)
            converted_y_right_lower = self.dxf2tk_convert_y(y_right_lower)

            # do vertical flip
            converted_y_left_upper = self.dxf2tk_vertical_flip(converted_y_left_upper)
            converted_y_right_lower = self.dxf2tk_vertical_flip(converted_y_right_lower)

            # Convert dxf start angle and extent of angle to tkinter
            start_angle = arc['start_angle']
            extent = 360 - (arc['start_angle'] - arc['end_angle'])

            self.converted_arcs.append(
                {
                    "x_left_upper": converted_x_left_upper,
                    "y_left_upper": converted_y_left_upper,
                    "x_right_lower": converted_x_right_lower,
                    "y_right_lower": converted_y_right_lower,
                    "start_angle": start_angle,
                    "extent": extent
                }
            )

        return self.converted_lines, self.converted_arcs
