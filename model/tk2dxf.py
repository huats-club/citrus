from app_parameters import app_parameters


class tk2dxf:
    def __init__(self, coverage):
        self.coverage = coverage

    def tk2dxf_convert_x(self, x):
        return int(x) / app_parameters.CANVAS_WIDTH * self.coverage.x_bound

    def tk2dxf_convert_y(self, y):
        return int(y) / app_parameters.CANVAS_HEIGHT * self.coverage.y_bound
