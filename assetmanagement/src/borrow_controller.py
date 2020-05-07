from datetime import date, timedelta

from PyQt5 import QtWidgets
from sqlalchemy.exc import IntegrityError

from borrow_view import BorrowView
from utils import error_message

class BorrowController:
    def __init__(self, model):
        self.dialog = QtWidgets.QDialog()
        self.view = BorrowView(self.dialog)
        self.model = model

        self.view.comboBox_Asset.currentIndexChanged \
            .connect(self.update_spinbox_range)
        self.view.buttonBox.accepted \
            .connect(self.borrow_asset)
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
            self.update_asset_combobox,
            pass_arguments=False
        )
        self.model.return_asset.add_observer(
            self.update_asset_combobox,
            pass_arguments=False
        )

    def run(self):
        self.reset()
        self.dialog.show()

    def reset(self):
        self.update_borrower_combobox()
        self.update_asset_combobox()
        self.update_spinbox_range()
        self.view.deselect_borrower_combobox()
        self.view.deselect_asset_combobox()
        self.view.clear_quantity_spinbox()

    def update_borrower_combobox(self):
        borrower_names = self.model.get_borrower_names(active_only=True)
        self.view.update_borrower_combobox(borrower_names)
        self.view.deselect_borrower_combobox()

    def update_asset_combobox(self):
        assets = self.model.get_assets(instock_only=True)
        asset_names = [asset[0] for asset in assets]
        self.view.update_asset_combobox(asset_names)
        self.view.deselect_asset_combobox()

    def update_spinbox_range(self):
        _, asset_name, _ = self.view.get_borrow_arguments()
        if asset_name is None:
            self.view.set_quantity_spinbox_range(0, 0)
        else:
            asset = self.model.get_asset(asset_name)
            # asset[1] is total, asset[2] is instock
            self.view.set_quantity_spinbox_range(1, asset[2])

    def borrow_asset(self):
        borrower_name, asset_name, quantity = self.view.get_borrow_arguments()
        datedue = date.today() + timedelta(days=7)
        # combobox ensures that NoResultFound will not be raised
        if borrower_name is None:
            error_message(
                self.dialog,
                'Please select a borrower.'
            )
            return
        if asset_name is None:
            error_message(
                self.dialog,
                'Please select an asset.'
            )
            return
        # exceptions avoided by spinbox range setting
        self.model.borrow_asset(
            borrower_name=borrower_name,
            asset_name=asset_name,
            quantity=quantity,
            datedue=datedue
        )
        self.dialog.accept()
