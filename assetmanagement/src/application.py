import sys

from PyQt5 import QtWidgets

from assetmanagement.src.main_controller import MainController

class Application:
    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.app.setApplicationName("Asset Management System")
        self.controller = MainController()

    def run(self):
        self.controller.run()
        sys.exit(self.app.exec_())
