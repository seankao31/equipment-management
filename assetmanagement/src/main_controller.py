from PyQt5 import QtWidgets

from assetmanagement.src.administrator_controller import \
    AdministratorController
from assetmanagement.src.asset_list_controller import AssetListController
from assetmanagement.src.borrow_controller import BorrowController
from assetmanagement.src.borrow_list_controller import BorrowListController
from assetmanagement.src.main_view import MainView
from assetmanagement.src.model import Model
from assetmanagement.src.return_controller import ReturnController


class MainController:
    def __init__(self):
        self.dialog = QtWidgets.QDialog()
        self.view = MainView(self.dialog)
        self.model = Model()
        self.administrator_controller = AdministratorController(self.model)
        self.borrow_list_controller = BorrowListController(self.model)
        self.asset_list_controller = AssetListController(self.model)
        self.borrow_controller = BorrowController(self.model)
        self.return_controller = ReturnController(self.model)

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

    def run(self):
        self.dialog.show()