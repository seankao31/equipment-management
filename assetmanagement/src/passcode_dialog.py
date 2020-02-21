# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'passcode_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_PasscodeDialog(object):
    def setupUi(self, PasscodeDialog):
        PasscodeDialog.setObjectName("PasscodeDialog")
        PasscodeDialog.resize(294, 111)
        self.gridLayout = QtWidgets.QGridLayout(PasscodeDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(PasscodeDialog)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.lineEdit = QtWidgets.QLineEdit(PasscodeDialog)
        self.lineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit.setObjectName("lineEdit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEdit)
        self.gridLayout.addLayout(self.formLayout, 1, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 0, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.pushButton = QtWidgets.QPushButton(PasscodeDialog)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_2.addWidget(self.pushButton)
        self.gridLayout.addLayout(self.horizontalLayout_2, 2, 0, 1, 1)

        self.retranslateUi(PasscodeDialog)
        QtCore.QMetaObject.connectSlotsByName(PasscodeDialog)

    def retranslateUi(self, PasscodeDialog):
        _translate = QtCore.QCoreApplication.translate
        PasscodeDialog.setWindowTitle(_translate("PasscodeDialog", "Passcode"))
        self.label.setText(_translate("PasscodeDialog", "passcode: "))
        self.pushButton.setText(_translate("PasscodeDialog", "OK"))
