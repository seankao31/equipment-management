from datetime import date, timedelta

from PyQt5 import QtWidgets
from sqlalchemy.exc import IntegrityError

from assetmanagement.src.borrow_view import BorrowView
from assetmanagement.src.utils import error_message

class BorrowController:
    def __init__(self, model):
        self.dialog = QtWidgets.QDialog()
        self.view = BorrowView(self.dialog)
        self.model = model

        self.view.buttonBox.accepted \
            .connect(self.borrow_asset)
        self.view.buttonBox.rejected \
            .connect(self.dialog.reject)

    def run(self):
        self.dialog.show()
        self.set_model()

    def set_model(self):
        self.view.comboBox_Borrower.clear()
        self.view.comboBox_Asset.clear()
        borrower_names = self.model.get_borrower_names(active_only=True)
        self.view.comboBox_Borrower.addItems(borrower_names)
        assets = self.model.get_assets(instock_only=True)
        asset_names = [asset[0] for asset in assets]
        self.view.comboBox_Asset.addItems(asset_names)

    def borrow_asset(self):
        borrower_name = self.view.comboBox_Borrower.currentText()
        asset_name = self.view.comboBox_Asset.currentText()
        quantity = self.view.spinBox_Quantity.value()
        datedue = date.today() + timedelta(days=7)
        # combobox ensures that NoResultFound will not be raised
        try:
            self.model.borrow_asset(
                borrower_name=borrower_name,
                asset_name=asset_name,
                quantity=quantity,
                datedue=datedue
            )
            self.dialog.accept()
        except ValueError:
            # can be avoided by setting spinbox range
            error_message(
                self.dialog,
                'Quantity should be positive.'
            )
        except IntegrityError:
            # can be avoided by setting combobox item
            error_message(
                self.dialog,
                'Not enough asset <{}> to be borrowed.'.format(asset_name)
            )
