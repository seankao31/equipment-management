from PyQt5 import QtCore, QtWidgets

from return_view import ReturnView

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
            assets = []
        else:
            loans = self.model.get_loans(
                borrower_name=borrower_name,
                active_only=True
            )
            count = dict()
            for loan in loans:
                asset_name = loan[1]
                quantity = loan[2]
                count[asset_name] = count.get(asset_name, 0) + quantity
            assets = list(k+' ({})'.format(v) for k, v in count.items())
            assets.sort()
        self.view.update_asset_list(assets)

    def return_asset(self):
        borrower_name, asset_names = self.view.get_return_arguments()
        for asset_name in asset_names:
            self.model.return_asset(borrower_name, asset_name)
        self.dialog.accept()
