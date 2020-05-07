from PyQt5 import QtWidgets

from passcode_view import PasscodeView
from utils import error_message

class PasscodeController:
    def __init__(self, model):
        self.dialog = QtWidgets.QDialog()
        self.view = PasscodeView(self.dialog)
        self.model = model

        self.view.pushButton.clicked \
            .connect(self.accept)

    def run(self):
        self.reset()
        self.dialog.exec_()

    def reset(self):
        self.view.clear_line_edit()

    def accept(self):
        passcode = self.view.get_passcode()
        if passcode and self.model.confirm_passcode(passcode):
            self.dialog.accept()
        else:
            error_message(
                self.dialog,
                'Passcode incorrect.'
            )
            self.reset()
