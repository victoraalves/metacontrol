# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Felipe\PycharmProjects\metacontrol\gui\views\ui_files\socresults.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1024, 720)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox_2 = QtWidgets.QGroupBox(Dialog)
        self.groupBox_2.setTitle("")
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.hMatrixTableView = QtWidgets.QTableView(self.groupBox_2)
        self.hMatrixTableView.setObjectName("hMatrixTableView")
        self.gridLayout_3.addWidget(self.hMatrixTableView, 1, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.groupBox_2)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout_3.addWidget(self.label_2, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox_2, 1, 0, 1, 3)
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.subsetSizeComboBox = QtWidgets.QComboBox(self.groupBox)
        self.subsetSizeComboBox.setObjectName("subsetSizeComboBox")
        self.gridLayout_2.addWidget(self.subsetSizeComboBox, 1, 2, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 1, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 1, 3, 1, 1)
        self.lossesTableView = QtWidgets.QTableView(self.groupBox)
        self.lossesTableView.setSortingEnabled(True)
        self.lossesTableView.setObjectName("lossesTableView")
        self.gridLayout_2.addWidget(self.lossesTableView, 2, 0, 1, 4)
        self.label = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 4)
        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 3)
        self.closeDialogPushButton = QtWidgets.QPushButton(Dialog)
        self.closeDialogPushButton.setObjectName("closeDialogPushButton")
        self.gridLayout.addWidget(self.closeDialogPushButton, 3, 2, 1, 1)
        self.reportPushButton = QtWidgets.QPushButton(Dialog)
        self.reportPushButton.setEnabled(False)
        self.reportPushButton.setObjectName("reportPushButton")
        self.gridLayout.addWidget(self.reportPushButton, 3, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 3, 0, 1, 1)
        self.groupBox_3 = QtWidgets.QGroupBox(Dialog)
        self.groupBox_3.setTitle("")
        self.groupBox_3.setObjectName("groupBox_3")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.groupBox_3)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.setNumberComboBox = QtWidgets.QComboBox(self.groupBox_3)
        self.setNumberComboBox.setObjectName("setNumberComboBox")
        self.gridLayout_4.addWidget(self.setNumberComboBox, 1, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.groupBox_3)
        self.label_5.setObjectName("label_5")
        self.gridLayout_4.addWidget(self.label_5, 1, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem2, 1, 2, 1, 1)
        self.sensitivityTableView = QtWidgets.QTableView(self.groupBox_3)
        self.sensitivityTableView.setObjectName("sensitivityTableView")
        self.gridLayout_4.addWidget(self.sensitivityTableView, 2, 0, 1, 3)
        self.label_3 = QtWidgets.QLabel(self.groupBox_3)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.gridLayout_4.addWidget(self.label_3, 0, 0, 1, 3)
        self.gridLayout.addWidget(self.groupBox_3, 2, 0, 1, 3)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_2.setText(_translate("Dialog", "H matrices"))
        self.label_4.setText(_translate("Dialog", "Subset size:"))
        self.label.setText(_translate("Dialog", "Control structures and losses evaluation"))
        self.closeDialogPushButton.setText(_translate("Dialog", "Close"))
        self.reportPushButton.setText(_translate("Dialog", "Generate report"))
        self.label_5.setText(_translate("Dialog", "Set number:"))
        self.label_3.setText(_translate("Dialog", "Sensitivity matrices (F)"))

