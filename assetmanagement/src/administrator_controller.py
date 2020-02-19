from PyQt5 import QtWidgets

from assetmanagement.src.administrator_view import AdministratorView

class AdministratorController:
    def __init__(self, model):
        self.dialog = QtWidgets.QDialog()
        self.view = AdministratorView(self.dialog)
        self.model = model

    def run(self):
        self.dialog.show()
