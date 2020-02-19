from PyQt5 import QtWidgets

def error_message(parent, message):
    QtWidgets.QMessageBox.warning(
        parent,
        'Error',
        message,
        QtWidgets.QMessageBox.Ok)