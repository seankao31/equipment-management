from PyQt5 import QtWidgets

from assetmanagement.src.asset_list_view import AssetListView

class AssetListController:
    def __init__(self, model):
        self.dialog = QtWidgets.QDialog()
        self.view = AssetListView(self.dialog)
        self.model = model

        self.view.checkBox_InstockOnly.stateChanged \
            .connect(self.update_table)
        self.view.buttonBox.rejected \
            .connect(self.dialog.reject)

        self.model.add_asset.add_observer(
            self.update_table,
            pass_arguments=False
        )
        self.model.remove_asset.add_observer(
            self.update_table,
            pass_arguments=False
        )
        self.model.borrow_asset.add_observer(
            self.update_table,
            pass_arguments=False
        )
        self.model.return_asset.add_observer(
            self.update_table,
            pass_arguments=False
        )

    def run(self):
        self.reset()
        self.dialog.show()

    def reset(self):
        self.view.clear_checkbox()
        self.update_table()

    def update_table(self):
        instock_only = self.view.get_instock_only()
        assets = self.model.get_assets(
            active_only=True,
            instock_only=instock_only
        )
        self.view.update_table(assets)
