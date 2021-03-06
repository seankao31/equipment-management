# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


import os, sys
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainDialog(object):
    def setupUi(self, MainDialog):
        MainDialog.setObjectName("MainDialog")
        MainDialog.resize(202, 300)
        self.gridLayout = QtWidgets.QGridLayout(MainDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.pushButton_Borrow = QtWidgets.QPushButton(MainDialog)
        self.pushButton_Borrow.setAutoDefault(False)
        self.pushButton_Borrow.setObjectName("pushButton_Borrow")
        self.verticalLayout.addWidget(self.pushButton_Borrow)
        self.pushButton_Return = QtWidgets.QPushButton(MainDialog)
        self.pushButton_Return.setAutoDefault(False)
        self.pushButton_Return.setObjectName("pushButton_Return")
        self.verticalLayout.addWidget(self.pushButton_Return)
        self.pushButton_BorrowList = QtWidgets.QPushButton(MainDialog)
        self.pushButton_BorrowList.setAutoDefault(False)
        self.pushButton_BorrowList.setObjectName("pushButton_BorrowList")
        self.verticalLayout.addWidget(self.pushButton_BorrowList)
        self.pushButton_AssetList = QtWidgets.QPushButton(MainDialog)
        self.pushButton_AssetList.setAutoDefault(False)
        self.pushButton_AssetList.setObjectName("pushButton_AssetList")
        self.verticalLayout.addWidget(self.pushButton_AssetList)
        self.pushButton_Administrator = QtWidgets.QPushButton(MainDialog)
        self.pushButton_Administrator.setAutoDefault(False)
        self.pushButton_Administrator.setObjectName("pushButton_Administrator")
        self.verticalLayout.addWidget(self.pushButton_Administrator)

        self.imageLabel = QtWidgets.QLabel(MainDialog)

        logo = self.resource_path('logo.png')
        pixmap = QtGui.QPixmap(logo)
        pixmap = pixmap.scaledToWidth(200, mode=QtCore.Qt.SmoothTransformation)
        self.imageLabel.setPixmap(pixmap)
        self.imageLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignBottom)
        self.verticalLayout.addWidget(self.imageLabel)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(MainDialog)
        QtCore.QMetaObject.connectSlotsByName(MainDialog)

    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    def retranslateUi(self, MainDialog):
        _translate = QtCore.QCoreApplication.translate
        MainDialog.setWindowTitle(_translate("MainDialog", "Equipment Management"))
        self.pushButton_Borrow.setText(_translate("MainDialog", "Borrow"))
        self.pushButton_Return.setText(_translate("MainDialog", "Return"))
        self.pushButton_BorrowList.setText(_translate("MainDialog", "Borrow List"))
        self.pushButton_AssetList.setText(_translate("MainDialog", "Equipment List"))
        self.pushButton_Administrator.setText(_translate("MainDialog", "Administrator"))
