# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'return_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ReturnDialog(object):
    def setupUi(self, ReturnDialog):
        ReturnDialog.setObjectName("ReturnDialog")
        ReturnDialog.resize(298, 299)
        self.verticalLayoutWidget = QtWidgets.QWidget(ReturnDialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 281, 281))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_Title = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.label_Title.setFont(font)
        self.label_Title.setObjectName("label_Title")
        self.verticalLayout.addWidget(self.label_Title)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label_Borrower = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_Borrower.setObjectName("label_Borrower")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_Borrower)
        self.label_Asset = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_Asset.setObjectName("label_Asset")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_Asset)
        self.comboBox_Borrower = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.comboBox_Borrower.setObjectName("comboBox_Borrower")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.comboBox_Borrower)
        self.listWidget_Asset = QtWidgets.QListWidget(self.verticalLayoutWidget)
        self.listWidget_Asset.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.listWidget_Asset.setObjectName("listWidget_Asset")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.listWidget_Asset)
        self.verticalLayout.addLayout(self.formLayout)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.buttonBox = QtWidgets.QDialogButtonBox(self.verticalLayoutWidget)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setText("Return")
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(ReturnDialog)
        QtCore.QMetaObject.connectSlotsByName(ReturnDialog)

    def retranslateUi(self, ReturnDialog):
        _translate = QtCore.QCoreApplication.translate
        ReturnDialog.setWindowTitle(_translate("ReturnDialog", "Return"))
        self.label_Title.setText(_translate("ReturnDialog", "Return"))
        self.label_Borrower.setText(_translate("ReturnDialog", "Borrower: "))
        self.label_Asset.setText(_translate("ReturnDialog", "Asset: "))
