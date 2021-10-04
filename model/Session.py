class Session:
    def __init__(self):
        self.current_plot_num = 1
        self.need_to_save = True

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

    def is_need_to_save(self):
        return self.need_to_save

    def set_need_to_save(self):
        self.need_to_save = True

    def set_no_need_to_save(self):
        self.need_to_save = False
