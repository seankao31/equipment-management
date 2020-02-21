from PyQt5 import QtWidgets

from assetmanagement.src.new_passcode_view import NewPasscodeView
from assetmanagement.src.utils import error_message

class NewPasscodeController:
    def __init__(self, model):
        self.dialog = QtWidgets.QDialog()
        self.view = NewPasscodeView(self.dialog)
        self.model = model

        self.view.pushButton.clicked \
            .connect(self.accept)
        # self.dialog.rejected \
        #     .connect(self.reject)

    def run(self):
        self.reset()
        return self.dialog.exec_()

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
