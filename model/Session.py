import os

from app_parameters import app_parameters


class Session:
    def __init__(self, session_name, session_workspace_folder, session_workspace_private):
        self.current_coverage_plot_num = 1
        self.current_coverage_save_num = 1
        self.current_spectrum_plot_num = 1
        self.current_recording_plot_num = 1
        self.need_to_save = True

        self.dxf_name = ""

        # session data
        self.session_name = session_name
        self.session_workspace_folder = os.getcwd() + '/' + session_workspace_folder
        self.session_private_folder = os.getcwd() + '/' + session_workspace_private

    def get_current_spectrum_plot_num(self):
        return self.current_spectrum_plot_num

    def increment_spectrum_plot_num(self):
        self.current_spectrum_plot_num += 1

    def get_current_coverage_plot_num(self):
        return self.current_coverage_plot_num

    def get_prev_coverage_plot_num(self):
        return self.current_coverage_plot_num - 1

    def increment_coverage_plot_num(self):
        self.current_coverage_plot_num += 1

    def get_current_coverage_save_num(self):
        return self.current_coverage_save_num

    def increment_coverage_save_num(self):
        self.current_coverage_save_num += 1

    def get_current_recording_plot_num(self):
        return self.current_recording_plot_num

    def increment_recording_plot_num(self):
        self.current_recording_plot_num += 1

    def save_dxf_name(self, name):
        self.dxf_name = name

    def get_dxf_prefix(self):
        return self.dxf_name

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
