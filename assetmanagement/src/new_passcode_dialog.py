# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'new_passcode_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_NewPasscodeDialog(object):
    def setupUi(self, NewPasscodeDialog):
        NewPasscodeDialog.setObjectName("NewPasscodeDialog")
        NewPasscodeDialog.resize(320, 140)
        self.gridLayout = QtWidgets.QGridLayout(NewPasscodeDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.pushButton = QtWidgets.QPushButton(NewPasscodeDialog)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_2.addWidget(self.pushButton)
        self.gridLayout.addLayout(self.horizontalLayout_2, 2, 0, 1, 1)
        self.formLayout_2 = QtWidgets.QFormLayout()
        self.formLayout_2.setObjectName("formLayout_2")
        self.label = QtWidgets.QLabel(NewPasscodeDialog)
        self.label.setObjectName("label")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.label_2 = QtWidgets.QLabel(NewPasscodeDialog)
        self.label_2.setObjectName("label_2")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.lineEdit_NewPasscode = QtWidgets.QLineEdit(NewPasscodeDialog)
        self.lineEdit_NewPasscode.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_NewPasscode.setObjectName("lineEdit_NewPasscode")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEdit_NewPasscode)
        self.lineEdit_ConfirmPasscode = QtWidgets.QLineEdit(NewPasscodeDialog)
        self.lineEdit_ConfirmPasscode.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_ConfirmPasscode.setObjectName("lineEdit_ConfirmPasscode")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lineEdit_ConfirmPasscode)
        self.gridLayout.addLayout(self.formLayout_2, 1, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 7, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 0, 0, 1, 1)

        self.retranslateUi(NewPasscodeDialog)
        QtCore.QMetaObject.connectSlotsByName(NewPasscodeDialog)

    def retranslateUi(self, NewPasscodeDialog):
        _translate = QtCore.QCoreApplication.translate
        NewPasscodeDialog.setWindowTitle(_translate("NewPasscodeDialog", "New Passcode"))
        self.pushButton.setText(_translate("NewPasscodeDialog", "OK"))
        self.label.setText(_translate("NewPasscodeDialog", "new passcode: "))
        self.label_2.setText(_translate("NewPasscodeDialog", "confirm passcode: "))
