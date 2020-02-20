from PyQt5 import QtWidgets

from assetmanagement.src.borrow_list_view import BorrowListView

class BorrowListController:
    def __init__(self, model):
        self.dialog = QtWidgets.QDialog()
        self.view = BorrowListView(self.dialog)
        self.model = model

        self.view.comboBox_Borrower.currentIndexChanged \
            .connect(self.update_table)
        self.view.pushButton_ClearBorrower.clicked \
            .connect(self.view.deselect_borrower_combobox)
        self.view.comboBox_Asset.currentIndexChanged \
            .connect(self.update_table)
        self.view.pushButton_ClearAsset.clicked \
            .connect(self.view.deselect_asset_combobox)
        self.view.radioButton_All.toggled \
            .connect(self.update_table)
        self.view.radioButton_Borrowing.toggled \
            .connect(self.update_table)
        self.view.radioButton_Overdue.toggled \
            .connect(self.update_table)
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
        self.model.add_asset.add_observer(
            self.update_asset_combobox,
            pass_arguments=False
        )
        self.model.remove_asset.add_observer(
            self.update_asset_combobox,
            pass_arguments=False
        )
        self.model.borrow_asset.add_observer(
            self.update_table,
            pass_arguments=False
        )
        self.model.return_asset.add_observer(
            self.update_table,
            pass_arguments=False
        )

    def run(self):
        self.reset()
        self.dialog.show()

    def reset(self):
        self.update_borrower_combobox()
        self.update_asset_combobox()
        self.view.deselect_borrower_combobox()
        self.view.deselect_asset_combobox()
        self.view.radioButton_All.setChecked(True)
        self.update_table()

    def update_borrower_combobox(self):
        borrower_names = self.model.get_borrower_names(active_only=True)
        self.view.update_borrower_combobox(borrower_names)
        self.view.deselect_borrower_combobox()

    def update_asset_combobox(self):
        assets = self.model.get_assets(active_only=True)
        asset_names = [asset[0] for asset in assets]
        self.view.update_asset_combobox(asset_names)
        self.view.deselect_borrower_combobox()

    def update_table(self):
        borrower_name, asset_name, active_only, overdue_only =\
            self.view.get_update_table_arguments()
        loans = self.model.get_loans(
            borrower_name=borrower_name,
            asset_name=asset_name,
            active_only=active_only,
            overdue_only=overdue_only
        )
        self.view.update_table(loans)
