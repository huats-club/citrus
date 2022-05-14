class Session:
    def __init__(self, session_name, session_relative_workspace_path, session_relative_private_path):
        self.session_name = session_name
        self.session_relative_workspace_path = session_relative_workspace_path
        self.session_relative_private_path = session_relative_private_path

        self.uuid = 0

        self.cached_floorplan_path = ""

    # Method returns the relative path from exe is called
    # e.g. workspace/timestamp
    def get_relative_workspace_path(self):
        return self.session_relative_workspace_path

    # Method returns the relative path to private cache folder from exe is called
    # e.g. workspace/timestamp/cache
    def get_relative_private_path(self):
        return self.session_relative_private_path

    def get_uuid(self):
        self.uuid += 1
        return self.uuid

    def set_cached_floorplan_path(self, path):
        self.cached_floorplan_path = path
