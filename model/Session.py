class Session:
    def __init__(self):
        self.current_plot_num = 1

    def get_current_plot_num(self):
        return self.current_plot_num

    def get_prev_plot_num(self):
        return self.current_plot_num - 1

    def increment_plot_num(self):
        self.current_plot_num += 1

    def save_dxf_name(self, name):
        self.name = name

    def get_dxf_prefix(self):
        return self.name
