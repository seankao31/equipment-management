from PyQt5 import QtWidgets

from assetmanagement.src.borrow_list_dialog import Ui_BorrowListDialog

class BorrowListView(Ui_BorrowListDialog):
    def __init__(self, parent):
        self.setupUi(parent)

    def deselect_borrower_combobox(self):
        self.comboBox_Borrower.setCurrentIndex(-1)

    def deselect_asset_combobox(self):
        self.comboBox_Asset.setCurrentIndex(-1)

    def update_borrower_combobox(self, borrower_names):
        self.comboBox_Borrower.clear()
        self.comboBox_Borrower.addItems(borrower_names)
        self.deselect_borrower_combobox()

    def update_asset_combobox(self, asset_names):
        self.comboBox_Asset.clear()
        self.comboBox_Asset.addItems(asset_names)
        self.deselect_borrower_combobox()

    def get_update_table_arguments(self):
        if self.comboBox_Borrower.currentIndex() == -1:
            borrower_name = None
        else:
            borrower_name = self.comboBox_Borrower.currentText()
        if self.comboBox_Asset.currentIndex() == -1:
            asset_name = None
        else:
            asset_name = self.comboBox_Asset.currentText()
        active_only = False
        overdue_only = False
        if self.radioButton_Borrowing.isChecked():
            active_only = True
        if self.radioButton_Overdue.isChecked():
            overdue_only = True
        return borrower_name, asset_name, active_only, overdue_only

    def update_table(self, loans):
        table = self.tableWidget
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
