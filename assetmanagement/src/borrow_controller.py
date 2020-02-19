from PyQt5 import QtWidgets

from assetmanagement.src.borrow_view import BorrowView

class BorrowController:
    def __init__(self, model):
        self.dialog = QtWidgets.QDialog()
        self.view = BorrowView(self.dialog)
        self.model = model

    def run(self):
        self.dialog.show()
