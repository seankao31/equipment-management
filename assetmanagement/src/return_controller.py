from PyQt5 import QtWidgets

from assetmanagement.src.return_view import ReturnView

class ReturnController:
    def __init__(self, model):
        self.dialog = QtWidgets.QDialog()
        self.view = ReturnView(self.dialog)
        self.model = model

    def run(self):
        self.dialog.show()
