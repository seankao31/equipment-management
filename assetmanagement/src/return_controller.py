from PyQt5 import QtCore, QtWidgets

from assetmanagement.src.return_view import ReturnView

class ReturnController:
    def __init__(self, model):
        self.dialog = QtWidgets.QDialog()
        self.view = ReturnView(self.dialog)
        self.model = model

        self.view.comboBox_Borrower.currentTextChanged \
            .connect(self.set_asset_list)
        self.view.buttonBox.accepted \
            .connect(self.return_asset)
        self.view.buttonBox.rejected \
            .connect(self.dialog.reject)

    def run(self):
        self.dialog.show()
        self.set_model()

    def set_model(self):
        self.view.comboBox_Borrower.clear()
        borrower_names = self.model.get_borrower_names(active_only=True)
        self.view.comboBox_Borrower.addItems(borrower_names)

    def set_asset_list(self):
        self.view.listWidget_Asset.clear()
        borrower_name = self.view.comboBox_Borrower.currentText()
        loans = self.model.get_loans(
            borrower_name=borrower_name,
            active_only=True
        )
        asset_names = list(set(loan[1] for loan in loans))
        asset_names.sort()
        self.view.listWidget_Asset.addItems(asset_names)

    def return_asset(self):
        borrower_name = self.view.comboBox_Borrower.currentText()
        selected_items = self.view.listWidget_Asset.selectedItems()
        for item in selected_items:
            self.model.return_asset(borrower_name, item.text())
        self.dialog.accept()
