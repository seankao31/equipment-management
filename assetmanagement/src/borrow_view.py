from borrow_dialog import Ui_BorrowDialog

class BorrowView(Ui_BorrowDialog):
    def __init__(self, parent):
        self.setupUi(parent)

    def deselect_borrower_combobox(self):
        self.comboBox_Borrower.setCurrentIndex(-1)

    def deselect_asset_combobox(self):
        self.comboBox_Asset.setCurrentIndex(-1)

    def clear_quantity_spinbox(self):
        self.spinBox_Quantity.setValue(self.spinBox_Quantity.minimum())

    def update_borrower_combobox(self, borrower_names):
        self.comboBox_Borrower.clear()
        self.comboBox_Borrower.addItems(borrower_names)

    def update_asset_combobox(self, asset_names):
        self.comboBox_Asset.clear()
        self.comboBox_Asset.addItems(asset_names)

    def get_borrow_arguments(self):
        if self.comboBox_Borrower.currentIndex() == -1:
            borrower_name = None
        else:
            borrower_name = self.comboBox_Borrower.currentText()
        if self.comboBox_Asset.currentIndex() == -1:
            asset_name = None
        else:
            asset_name = self.comboBox_Asset.currentText()
        quantity = self.spinBox_Quantity.value()
        return borrower_name, asset_name, quantity

    def set_quantity_spinbox_range(self, minimum, maximum):
        self.spinBox_Quantity.setMinimum(minimum)
        self.spinBox_Quantity.setMaximum(maximum)
