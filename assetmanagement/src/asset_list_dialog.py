# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'asset_list_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AssetListDialog(object):
    def setupUi(self, AssetListDialog):
        AssetListDialog.setObjectName("AssetListDialog")
        AssetListDialog.resize(349, 346)
        self.gridLayout = QtWidgets.QGridLayout(AssetListDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_Title = QtWidgets.QLabel(AssetListDialog)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.label_Title.setFont(font)
        self.label_Title.setObjectName("label_Title")
        self.verticalLayout.addWidget(self.label_Title)
        self.checkBox_InstockOnly = QtWidgets.QCheckBox(AssetListDialog)
        self.checkBox_InstockOnly.setObjectName("checkBox_InstockOnly")
        self.verticalLayout.addWidget(self.checkBox_InstockOnly)
        self.tableWidget = QtWidgets.QTableWidget(AssetListDialog)
        self.tableWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        self.verticalLayout.addWidget(self.tableWidget)
        self.buttonBox = QtWidgets.QDialogButtonBox(AssetListDialog)
        self.pushButton_Close = QtWidgets.QPushButton()
        self.pushButton_Close.setAutoDefault(False)
        self.pushButton_Close.setObjectName("pushButton_Close")
        self.buttonBox.addButton(self.pushButton_Close, QtWidgets.QDialogButtonBox.RejectRole)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(AssetListDialog)
        QtCore.QMetaObject.connectSlotsByName(AssetListDialog)

    def retranslateUi(self, AssetListDialog):
        _translate = QtCore.QCoreApplication.translate
        AssetListDialog.setWindowTitle(_translate("AssetListDialog", "Equipment List"))
        self.label_Title.setText(_translate("AssetListDialog", "Equipment List"))
        self.checkBox_InstockOnly.setText(_translate("AssetListDialog", "In stock only"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("AssetListDialog", "Name"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("AssetListDialog", "Total"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("AssetListDialog", "In Stock"))
        self.pushButton_Close.setText(_translate("AdministratorDialog", "Close"))
