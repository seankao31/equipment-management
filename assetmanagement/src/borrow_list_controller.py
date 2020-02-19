from PyQt5 import QtCore, QtWidgets

from assetmanagement.src.borrow_list_view import BorrowListView

class BorrowListController:
    def __init__(self, model):
        self.dialog = QtWidgets.QDialog()
        self.view = BorrowListView(self.dialog)
        self.model = model

        self.view.comboBox_Borrower.currentIndexChanged \
            .connect(self.update_table)
        self.view.pushButton_ClearBorrower.clicked \
            .connect(self.deselect_borrower)
        self.view.comboBox_Asset.currentIndexChanged \
            .connect(self.update_table)
        self.view.pushButton_ClearAsset.clicked \
            .connect(self.deselect_asset)
        self.view.radioButton_All.toggled \
            .connect(self.update_table)
        self.view.radioButton_Borrowing.toggled \
            .connect(self.update_table)
        self.view.radioButton_Overdue.toggled \
            .connect(self.update_table)
        self.view.buttonBox.rejected \
            .connect(self.dialog.reject)

    def run(self):
        self.dialog.show()
        self.set_model()

    def set_model(self):
        self.view.comboBox_Borrower.clear()
        borrower_names = self.model.get_borrower_names(active_only=True)
        self.view.comboBox_Borrower.addItems(borrower_names)
        self.deselect_borrower()

        self.view.comboBox_Asset.clear()
        assets = self.model.get_assets(active_only=True)
        asset_names = [asset[0] for asset in assets]
        self.view.comboBox_Asset.addItems(asset_names)
        self.deselect_asset()

        self.update_table()

    def update_table(self):
        if self.view.comboBox_Borrower.currentIndex() == -1:
            borrower_name = None
        else:
            borrower_name = self.view.comboBox_Borrower.currentText()
        if self.view.comboBox_Asset.currentIndex() == -1:
            asset_name = None
        else:
            asset_name = self.view.comboBox_Asset.currentText()
        active_only = False
        overdue_only = False
        if self.view.radioButton_Borrowing.isChecked():
            active_only = True
        if self.view.radioButton_Overdue.isChecked():
            overdue_only = True

        loans = self.model.get_loans(
            borrower_name=borrower_name,
            asset_name=asset_name,
            active_only=active_only,
            overdue_only=overdue_only
        )
        table = self.view.tableWidget
        table.clearContents()
        table.setRowCount(0)
        for row, loan in enumerate(loans):
            table.insertRow(row)
            table.setItem(row, 0, \
                QtWidgets.QTableWidgetItem(loan[0]))
            table.setItem(row, 1, \
                QtWidgets.QTableWidgetItem(loan[1]))
            table.setItem(row, 2, \
                QtWidgets.QTableWidgetItem(str(loan[2])))
            table.setItem(row, 3, \
                QtWidgets.QTableWidgetItem(loan[3].strftime("%Y-%m-%d")))
            table.setItem(row, 4, \
                QtWidgets.QTableWidgetItem('Yes' if loan[4] else 'No'))

    def deselect_borrower(self):
        self.view.comboBox_Borrower.setCurrentIndex(-1)

    def deselect_asset(self):
        self.view.comboBox_Asset.setCurrentIndex(-1)
