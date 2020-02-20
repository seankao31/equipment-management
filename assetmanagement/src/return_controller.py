from PyQt5 import QtCore, QtWidgets

from assetmanagement.src.return_view import ReturnView

class ReturnController:
    def __init__(self, model):
        self.dialog = QtWidgets.QDialog()
        self.view = ReturnView(self.dialog)
        self.model = model

        self.view.comboBox_Borrower.currentIndexChanged \
            .connect(self.update_asset_list)
        self.view.buttonBox.accepted \
            .connect(self.return_asset)
        self.view.buttonBox.rejected \
            .connect(self.dialog.reject)

        self.model.add_borrower.add_observer(
            self.update_borrower_combobox,
            pass_arguments=False
        )
        self.model.deactivate_borrower.add_observer(
            self.update_borrower_combobox,
            pass_arguments=False
        )
        self.model.borrow_asset.add_observer(
            self.update_asset_list,
            pass_arguments=False
        )
        self.model.return_asset.add_observer(
            self.update_asset_list,
            pass_arguments=False
        )

    def run(self):
        self.reset()
        self.dialog.show()

    def reset(self):
        self.update_borrower_combobox()
        self.view.deselect_borrower_combobox()
        self.update_asset_list()

    def update_borrower_combobox(self):
        borrower_names = self.model.get_borrower_names(active_only=True)
        self.view.update_borrower_combobox(borrower_names)

    def update_asset_list(self):
        borrower_name = self.view.get_borrower_name()
        if borrower_name is None:
            asset_names = []
        else:
            loans = self.model.get_loans(
                borrower_name=borrower_name,
                active_only=True
            )
            asset_names = list(set(loan[1] for loan in loans))
            asset_names.sort()
        self.view.update_asset_list(asset_names)

    def return_asset(self):
        borrower_name = self.view.comboBox_Borrower.currentText()
        selected_items = self.view.listWidget_Asset.selectedItems()
        for item in selected_items:
            self.model.return_asset(borrower_name, item.text())
        self.dialog.accept()
