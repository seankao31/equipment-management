from PyQt5 import QtWidgets
from sqlalchemy.exc import IntegrityError

from administrator_view import AdministratorView
from model import ModelError
from new_passcode_controller import NewPasscodeController
from passcode_controller import PasscodeController
from utils import error_message

class AdministratorController:
    def __init__(self, model):
        self.dialog = QtWidgets.QDialog()
        self.view = AdministratorView(self.dialog)
        self.model = model

        self.view.pushButton_ChangePasscode.clicked \
            .connect(self.change_passcode_verify)
        self.view.pushButton_AddBorrower.clicked \
            .connect(self.add_borrower)
        self.view.pushButton_RemoveBorrower.clicked \
            .connect(self.remove_borrower)
        self.view.pushButton_AddAsset.clicked \
            .connect(self.add_asset)
        self.view.comboBox_Asset.currentIndexChanged \
            .connect(self.update_spinbox_max)
        self.view.pushButton_RemoveAsset.clicked \
            .connect(self.remove_asset)
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

    def change_passcode_verify(self):
        self.passcode_controller = PasscodeController(self.model)
        self.passcode_controller.dialog.accepted \
            .connect(self.change_passcode_update)
        # self.passcode_controller.dialog.rejected \
        #     .connect(sys.exit)
        self.passcode_controller.run()

    def change_passcode_update(self):
        self.new_passcode_controller = NewPasscodeController(self.model)
        # self.new_passcode_controller.dialog.accepted \
        #     .connect(self.enter)
        # self.new_passcode_controller.dialog.rejected \
        #     .connect(sys.exit)
        self.new_passcode_controller.run()

    def run(self):
        self.reset()
        self.dialog.show()

    def reset(self):
        self.update_borrower_combobox()
        self.update_asset_combobox()
        self.view.clear_borrower_line_edit()
        self.view.deselect_borrower_combobox()
        self.view.clear_asset_line_edit()
        self.view.clear_add_asset_spinbox()
        self.view.deselect_asset_combobox()
        self.view.clear_remove_asset_spinbox()

    def update_borrower_combobox(self):
        borrower_names = self.model.get_borrower_names(active_only=True)
        self.view.update_borrower_combobox(borrower_names)
        self.view.deselect_borrower_combobox()

    def update_asset_combobox(self):
        assets = self.model.get_assets(active_only=True)
        asset_names = [asset[0] for asset in assets]
        self.view.update_asset_combobox(asset_names)
        self.view.deselect_asset_combobox()

    def add_borrower(self):
        borrower_name = self.view.get_borrower_name_to_add()
        try:
            self.model.add_borrower(borrower_name)
            self.view.clear_borrower_line_edit()
        except IntegrityError:
            error_message(
                self.dialog,
                'Borrower <{}> already exists.'.format(borrower_name)
            )

    def remove_borrower(self):
        borrower_name = self.view.get_borrower_name_to_remove()
        if borrower_name is None:
            error_message(
                self.dialog,
                'Please select a borrower.'
            )
            return
        try:
            self.model.deactivate_borrower(borrower_name)
            self.view.deselect_borrower_combobox()
            # Combobox ensures that NoResultFound will not be raised.
        except ModelError:
            # This error can be avoided by proper combobox item setting.
            # However, leaving it as is might be more user friendly.
            error_message(
                self.dialog,
                'Borrower <{}> has not returned all assets.'.format(
                    borrower_name)
            )

    def add_asset(self):
        asset_name, quantity = self.view.get_add_asset_arguments()
        # Spinbox ensures that the number is non negative.
        self.model.add_asset(asset_name, quantity)
        self.view.clear_asset_line_edit()
        self.view.clear_add_asset_spinbox()

    def update_spinbox_max(self):
        asset_name, _ = self.view.get_remove_asset_arguments()
        if asset_name is None:
            self.view.set_remove_asset_spinbox_maximum(0)
        else:
            asset = self.model.get_asset(asset_name)
            # asset[1] is total, asset[2] is instock
            self.view.set_remove_asset_spinbox_maximum(asset[1])

    def remove_asset(self):
        asset_name, quantity = self.view.get_remove_asset_arguments()
        if asset_name is None:
            error_message(
                self.dialog,
                'Please select an asset.'
            )
            return
        # Comboxbox ensures that NoResultFound will not be raised.
        # Spinbox ensures that the number is non negative.
        try:
            self.model.remove_asset(asset_name, quantity)
            self.view.clear_remove_asset_spinbox()
        except IntegrityError:
            # This error can be avoided by proper combobox item setting
            # and proper spinbox range. However, leaving as is might be
            # more user friendly.
            error_message(
                self.dialog,
                ('Not enough asset <{}> to be removed. '
                 'Some might be borrowed.'.format(asset_name))
            )
