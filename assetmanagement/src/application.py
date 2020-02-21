import sys

from PyQt5 import QtWidgets

from assetmanagement.src.main_controller import MainController
from assetmanagement.src.model import Model

class Application:
    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.app.setApplicationName("Asset Management System")
        self.model = Model()
        self.controller = MainController(self.model)

    def run(self):
        self.controller.run()
        sys.exit(self.app.exec_())
