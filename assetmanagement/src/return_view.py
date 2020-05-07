from return_dialog import Ui_ReturnDialog

class ReturnView(Ui_ReturnDialog):
    def __init__(self, parent):
        self.setupUi(parent)

    def deselect_borrower_combobox(self):
        self.comboBox_Borrower.setCurrentIndex(-1)

    def update_borrower_combobox(self, borrower_names):
        self.comboBox_Borrower.clear()
        self.comboBox_Borrower.addItems(borrower_names)

    def update_asset_list(self, assets):
        self.listWidget_Asset.clear()
        self.listWidget_Asset.addItems(assets)

    def get_borrower_name(self):
        if self.comboBox_Borrower.currentIndex() == -1:
            borrower_name = None
        else:
            borrower_name = self.comboBox_Borrower.currentText()
        return borrower_name

    def get_return_arguments(self):
        borrower_name = self.comboBox_Borrower.currentText()
        selected_items = self.listWidget_Asset.selectedItems()
        asset_names = []
        for item in selected_items:
            text = item.text()
            i = text.rfind('(')
            i -= 1
            asset_name = text[:i]
            asset_names.append(asset_name)
        return borrower_name, asset_names
