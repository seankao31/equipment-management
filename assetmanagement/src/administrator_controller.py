from PyQt5 import QtWidgets
from sqlalchemy.exc import IntegrityError

from assetmanagement.src.administrator_view import AdministratorView
from assetmanagement.src.utils import error_message

class AdministratorController:
    def __init__(self, model):
        self.dialog = QtWidgets.QDialog()
        self.view = AdministratorView(self.dialog)
        self.model = model

        self.view.pushButton_AddBorrower.clicked \
            .connect(self.add_borrower)
        self.view.pushButton_RemoveBorrower.clicked \
            .connect(self.remove_borrower)
        self.view.pushButton_AddAsset.clicked \
            .connect(self.add_asset)
        self.view.pushButton_RemoveAsset.clicked \
            .connect(self.remove_asset)
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
        assets = self.model.get_assets(active_only=True)
        asset_names = [asset[0] for asset in assets]
        self.view.comboBox_Asset.addItems(asset_names)

    def add_borrower(self):
        borrower_name = self.view.lineEdit_Borrower.text()
        try:
            self.model.add_borrower(borrower_name)
            self.view.lineEdit_Borrower.setText('')
            self.set_model()
        except IntegrityError:
            error_message(
                self.dialog,
                'Borrower <{}> already exists.'.format(borrower_name)
            )

    def remove_borrower(self):
        borrower_name = self.view.comboBox_Borrower.currentText()
        try:
            self.model.deactivate_borrower(borrower_name)
            self.set_model()
            # combobox ensures that NoResultFound will not be raised
        except IntegrityError:
            # this error can be avoided by proper combobox item setting
            error_message(
                self.dialog,
                'Borrower <{}> has not returned all assets.'.format(
                    borrower_name)
            )

    def add_asset(self):
        asset_name = self.view.lineEdit_Asset.text()
        quantity = self.view.spinBox_AddAsset.value()
        # spinbox ensures that the number is non negative
        self.model.add_asset(asset_name, quantity)
        self.view.lineEdit_Asset.setText('')
        self.view.spinBox_AddAsset.setValue(0)
        self.set_model()

    def remove_asset(self):
        asset_name = self.view.comboBox_Asset.currentText()
        quantity = self.view.spinBox_RemoveAsset.value()
        # comboxbox ensures that NoResultFound will not be raised
        # spinbox ensures that the number is non negative
        try:
            self.model.remove_asset(asset_name, quantity)
            self.set_model()
        except IntegrityError:
            # this error can be avoided by proper combobox item setting
            # and proper spinbox range
            error_message(
                self.dialog,
                'Not enough asset <{}> to be removed.'.format(asset_name)
            )