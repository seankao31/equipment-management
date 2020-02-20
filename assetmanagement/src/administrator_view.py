from assetmanagement.src.administrator_dialog import Ui_AdministratorDialog

class AdministratorView(Ui_AdministratorDialog):
    def __init__(self, parent):
        self.setupUi(parent)

    def clear_borrower_line_edit(self):
        self.lineEdit_Borrower.setText('')

    def deselect_borrower_combobox(self):
        self.comboBox_Borrower.setCurrentIndex(-1)

    def clear_asset_line_edit(self):
        self.lineEdit_Asset.setText('')

    def clear_add_asset_spinbox(self):
        self.spinBox_AddAsset.setValue(self.spinBox_AddAsset.minimum())

    def deselect_asset_combobox(self):
        self.comboBox_Asset.setCurrentIndex(-1)

    def clear_remove_asset_spinbox(self):
        self.spinBox_RemoveAsset.setValue(self.spinBox_RemoveAsset.minimum())

    def update_borrower_combobox(self, borrower_names):
        self.comboBox_Borrower.clear()
        self.comboBox_Borrower.addItems(borrower_names)

    def update_asset_combobox(self, asset_names):
        self.comboBox_Asset.clear()
        self.comboBox_Asset.addItems(asset_names)

    def get_borrower_name_to_add(self):
        return self.lineEdit_Borrower.text()

    def get_borrower_name_to_remove(self):
        if self.comboBox_Borrower.currentIndex() == -1:
            borrower_name = None
        else:
            borrower_name = self.comboBox_Borrower.currentText()
        return borrower_name

    def get_add_asset_arguments(self):
        asset_name = self.lineEdit_Asset.text()
        quantity = self.spinBox_AddAsset.value()
        return asset_name, quantity

    def get_remove_asset_arguments(self):
        if self.comboBox_Asset.currentIndex() == -1:
            asset_name = None
        else:
            asset_name = self.comboBox_Asset.currentText()
        quantity = self.spinBox_RemoveAsset.value()
        return asset_name, quantity

    def set_remove_asset_spinbox_maximum(self, maximum):
        self.spinBox_RemoveAsset.setMaximum(maximum)
