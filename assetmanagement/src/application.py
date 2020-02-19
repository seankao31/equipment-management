from PyQt5 import QtWidgets

from assetmanagement.src.main_controller import MainController

class Application:
    def __init__(self):
        self.app = QtWidgets.QApplication([])
        self.controller = MainController()

    def run(self):
        self.controller.run()
        self.app.exec_()
