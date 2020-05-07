import sys

from PyQt5 import QtGui, QtWidgets

from main_controller import MainController
from model import Model

class Application:
    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.app.setFont(font)
        self.app.setApplicationName("Equipment Management System")
        self.model = Model()
        self.controller = MainController(self.model)

    def run(self):
        self.controller.run()
        sys.exit(self.app.exec_())
