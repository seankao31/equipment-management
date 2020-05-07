from PyQt5 import QtWidgets

from new_passcode_view import NewPasscodeView
from utils import error_message

class NewPasscodeController:
    def __init__(self, model):
        self.dialog = QtWidgets.QDialog()
        self.view = NewPasscodeView(self.dialog)
        self.model = model

        self.view.pushButton.clicked \
            .connect(self.accept)

    def run(self):
        self.reset()
        self.dialog.exec_()

    def reset(self):
        self.view.clear_new_passcode_line_edit()
        self.view.clear_confirm_passcode_line_edit()

    def accept(self):
        new_passcode, confirm_passcode = self.view.get_arguments()
        if new_passcode and new_passcode == confirm_passcode:
            self.model.new_passcode(new_passcode)
            self.dialog.accept()
        else:
            error_message(
                self.dialog,
                'Confirm passcode does not match new passcode.'
            )
            self.reset()
