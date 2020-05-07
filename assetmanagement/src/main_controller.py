import sys

from PyQt5 import QtWidgets

from administrator_controller import \
    AdministratorController
from asset_list_controller import AssetListController
from borrow_controller import BorrowController
from borrow_list_controller import BorrowListController
from main_view import MainView
from new_passcode_controller import NewPasscodeController
from passcode_controller import PasscodeController
from return_controller import ReturnController


class MainController:
    def __init__(self, model):
        self.dialog = QtWidgets.QDialog()
        self.view = MainView(self.dialog)
        self.model = model
        self.administrator_controller = AdministratorController(model)
        self.borrow_list_controller = BorrowListController(model)
        self.asset_list_controller = AssetListController(model)
        self.borrow_controller = BorrowController(model)
        self.return_controller = ReturnController(model)

        self.view.pushButton_Administrator.clicked \
            .connect(self.administrator_controller.run)
        self.view.pushButton_BorrowList.clicked \
            .connect(self.borrow_list_controller.run)
        self.view.pushButton_AssetList.clicked \
            .connect(self.asset_list_controller.run)
        self.view.pushButton_Borrow.clicked \
            .connect(self.borrow_controller.run)
        self.view.pushButton_Return.clicked \
            .connect(self.return_controller.run)

    def verify(self):
        if self.model.exist_passcode():
            self.passcode_controller = PasscodeController(self.model)
            self.passcode_controller.dialog.accepted \
                .connect(self.enter)
            self.passcode_controller.dialog.rejected \
                .connect(sys.exit)
            self.passcode_controller.run()
        else:
            self.new_passcode_controller = NewPasscodeController(self.model)
            self.new_passcode_controller.dialog.accepted \
                .connect(self.enter)
            self.new_passcode_controller.dialog.rejected \
                .connect(sys.exit)
            self.new_passcode_controller.run()

    def run(self):
        self.verify()

    def enter(self):
        self.dialog.show()
