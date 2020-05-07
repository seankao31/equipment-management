from new_passcode_dialog import Ui_NewPasscodeDialog

class NewPasscodeView(Ui_NewPasscodeDialog):
    def __init__(self, parent):
        self.setupUi(parent)

    def clear_new_passcode_line_edit(self):
        self.lineEdit_NewPasscode.setText('')

    def clear_confirm_passcode_line_edit(self):
        self.lineEdit_ConfirmPasscode.setText('')

    def get_arguments(self):
        new_passcode = self.lineEdit_NewPasscode.text()
        confirm_passcode = self.lineEdit_ConfirmPasscode.text()
        return new_passcode, confirm_passcode
