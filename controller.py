class Controller():
    def __init__(self, root):

        # Store tkinter root object
        self.gui = root

    def on_exit(self):
        # Destroy entire window to exit
        print("Exiting...")
        self.gui.destroy()
