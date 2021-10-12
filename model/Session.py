from app_parameters import app_parameters


class Session:
    def __init__(self, session_name):
        self.current_plot_num = 1
        self.need_to_save = True

        # session data
        self.session_name = session_name
        self.session_workspace_folder = app_parameters.WORKSPACE_FOLDER + f"/{session_name}"
        self.session_private_folder = app_parameters.PRIVATE_FOLDER + f"/{session_name}"

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

    def get_session_workspace_path(self):
        return self.session_workspace_folder

    def get_session_private_folder_path(self):
        return self.session_private_folder
