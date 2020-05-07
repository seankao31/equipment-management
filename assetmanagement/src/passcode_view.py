from passcode_dialog import Ui_PasscodeDialog

class PasscodeView(Ui_PasscodeDialog):
    def __init__(self, parent):
        self.setupUi(parent)

    def clear_line_edit(self):
        self.lineEdit.setText('')

    def get_passcode(self):
        return self.lineEdit.text()
