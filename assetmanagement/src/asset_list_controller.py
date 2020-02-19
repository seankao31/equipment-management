from PyQt5 import QtWidgets

from assetmanagement.src.asset_list_view import AssetListView

class AssetListController:
    def __init__(self, model):
        self.dialog = QtWidgets.QDialog()
        self.view = AssetListView(self.dialog)
        self.model = model

        self.view.checkBox_InstockOnly.stateChanged \
            .connect(self.set_model)
        self.view.buttonBox.rejected \
            .connect(self.dialog.reject)

    def run(self):
        self.dialog.show()
        self.set_model()

    def set_model(self):
        instock_only = self.view.checkBox_InstockOnly.isChecked()
        assets = self.model.get_assets(
            active_only=True,
            instock_only=instock_only
        )
        table = self.view.tableWidget
        table.clearContents()
        table.setRowCount(0)
        for row, asset in enumerate(assets):
            table.insertRow(row)
            table.setItem(row, 0, QtWidgets.QTableWidgetItem(asset[0]))
            table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(asset[1])))
            table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(asset[2])))
