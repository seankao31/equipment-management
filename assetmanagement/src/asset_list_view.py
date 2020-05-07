from PyQt5 import QtWidgets

from asset_list_dialog import Ui_AssetListDialog

class AssetListView(Ui_AssetListDialog):
    def __init__(self, parent):
        self.setupUi(parent)

    def clear_checkbox(self):
        self.checkBox_InstockOnly.setChecked(False)

    def get_instock_only(self):
        return self.checkBox_InstockOnly.isChecked()

    def update_table(self, assets):
        table = self.tableWidget
        table.clearContents()
        table.setRowCount(0)
        for row, asset in enumerate(assets):
            table.insertRow(row)
            table.setItem(row, 0, QtWidgets.QTableWidgetItem(asset[0]))
            table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(asset[1])))
            table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(asset[2])))
