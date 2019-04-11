# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_files\mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1026, 859)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setWhatsThis("")
        MainWindow.setStyleSheet("")
        MainWindow.setDockOptions(QtWidgets.QMainWindow.AllowTabbedDocks|QtWidgets.QMainWindow.AnimatedDocks)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setAutoFillBackground(True)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.tabMainWidget = QtWidgets.QTabWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabMainWidget.sizePolicy().hasHeightForWidth())
        self.tabMainWidget.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.tabMainWidget.setFont(font)
        self.tabMainWidget.setStyleSheet("QTabWidget::setTabIcon(0, QIcon(\'Screenshot.png\'))")
        self.tabMainWidget.setTabPosition(QtWidgets.QTabWidget.West)
        self.tabMainWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabMainWidget.setTabsClosable(False)
        self.tabMainWidget.setObjectName("tabMainWidget")
        self.simulationTab = QtWidgets.QWidget()
        self.simulationTab.setEnabled(True)
        self.simulationTab.setStyleSheet("")
        self.simulationTab.setObjectName("simulationTab")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.simulationTab)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.groupBox = QtWidgets.QGroupBox(self.simulationTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setMinimumSize(QtCore.QSize(475, 500))
        self.groupBox.setMaximumSize(QtCore.QSize(800, 16777215))
        self.groupBox.setStyleSheet("QGroupBox {\n"
"    border: 1px solid gray;\n"
"    border-radius: 9px;\n"
"    font-weight: bold;\n"
"}\n"
"\n"
"QGroupBox::title {\n"
"    subcontrol-origin: margin;\n"
"    left: 10px;\n"
"    top: 5px;\n"
"    padding: 0 3px 0 3px;\n"
"}")
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.buttonOpenSimFile = QtWidgets.QPushButton(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonOpenSimFile.sizePolicy().hasHeightForWidth())
        self.buttonOpenSimFile.setSizePolicy(sizePolicy)
        self.buttonOpenSimFile.setMinimumSize(QtCore.QSize(120, 30))
        self.buttonOpenSimFile.setMaximumSize(QtCore.QSize(120, 30))
        self.buttonOpenSimFile.setStatusTip("")
        self.buttonOpenSimFile.setWhatsThis("")
        self.buttonOpenSimFile.setObjectName("buttonOpenSimFile")
        self.gridLayout.addWidget(self.buttonOpenSimFile, 1, 2, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem, 3, 1, 1, 1)
        self.buttonLoadVariables = QtWidgets.QPushButton(self.groupBox)
        self.buttonLoadVariables.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonLoadVariables.sizePolicy().hasHeightForWidth())
        self.buttonLoadVariables.setSizePolicy(sizePolicy)
        self.buttonLoadVariables.setMinimumSize(QtCore.QSize(120, 30))
        self.buttonLoadVariables.setObjectName("buttonLoadVariables")
        self.gridLayout.addWidget(self.buttonLoadVariables, 2, 2, 1, 1)
        self.tableWidgetAliasDisplay = QtWidgets.QTableWidget(self.groupBox)
        self.tableWidgetAliasDisplay.setObjectName("tableWidgetAliasDisplay")
        self.tableWidgetAliasDisplay.setColumnCount(2)
        self.tableWidgetAliasDisplay.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidgetAliasDisplay.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidgetAliasDisplay.setHorizontalHeaderItem(1, item)
        self.tableWidgetAliasDisplay.horizontalHeader().setStretchLastSection(True)
        self.gridLayout.addWidget(self.tableWidgetAliasDisplay, 5, 1, 1, 2)
        self.textBrowserSimFile = QtWidgets.QTextBrowser(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textBrowserSimFile.sizePolicy().hasHeightForWidth())
        self.textBrowserSimFile.setSizePolicy(sizePolicy)
        self.textBrowserSimFile.setMinimumSize(QtCore.QSize(300, 75))
        self.textBrowserSimFile.setStyleSheet("")
        self.textBrowserSimFile.setObjectName("textBrowserSimFile")
        self.gridLayout.addWidget(self.textBrowserSimFile, 1, 1, 2, 1)
        spacerItem1 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 3, 1, 1)
        self.label_13 = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_13.setFont(font)
        self.label_13.setObjectName("label_13")
        self.gridLayout.addWidget(self.label_13, 0, 1, 1, 1)
        self.label_11 = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")
        self.gridLayout.addWidget(self.label_11, 4, 1, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem2, 6, 1, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem3, 1, 0, 1, 1)
        self.gridLayout_6.addWidget(self.groupBox, 0, 0, 1, 1)
        self.groupBox_2 = QtWidgets.QGroupBox(self.simulationTab)
        self.groupBox_2.setMinimumSize(QtCore.QSize(475, 500))
        self.groupBox_2.setStyleSheet("QGroupBox {\n"
"    border: 1px solid gray;\n"
"    border-radius: 9px;\n"
"    font-weight: bold;\n"
"}\n"
"\n"
"QGroupBox::title {\n"
"    subcontrol-origin: margin;\n"
"    left: 10px;\n"
"    top: 5px;\n"
"    padding: 0 3px 0 3px;\n"
"}")
        self.groupBox_2.setTitle("")
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_3.setObjectName("gridLayout_3")
        spacerItem4 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem4, 1, 2, 1, 1)
        spacerItem5 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem5, 1, 0, 1, 1)
        spacerItem6 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout_3.addItem(spacerItem6, 2, 1, 1, 1)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.groupBox_2)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.lineEditComponents = QtWidgets.QLineEdit(self.groupBox_2)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.lineEditComponents.setFont(font)
        self.lineEditComponents.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEditComponents.setReadOnly(True)
        self.lineEditComponents.setObjectName("lineEditComponents")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEditComponents)
        self.label_2 = QtWidgets.QLabel(self.groupBox_2)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.lineEditMethodName = QtWidgets.QLineEdit(self.groupBox_2)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.lineEditMethodName.setFont(font)
        self.lineEditMethodName.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEditMethodName.setReadOnly(True)
        self.lineEditMethodName.setObjectName("lineEditMethodName")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lineEditMethodName)
        self.label_3 = QtWidgets.QLabel(self.groupBox_2)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.lineEditBlocks = QtWidgets.QLineEdit(self.groupBox_2)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.lineEditBlocks.setFont(font)
        self.lineEditBlocks.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEditBlocks.setReadOnly(True)
        self.lineEditBlocks.setObjectName("lineEditBlocks")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.lineEditBlocks)
        self.label_4 = QtWidgets.QLabel(self.groupBox_2)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.lineEditStreams = QtWidgets.QLineEdit(self.groupBox_2)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.lineEditStreams.setFont(font)
        self.lineEditStreams.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEditStreams.setReadOnly(True)
        self.lineEditStreams.setObjectName("lineEditStreams")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.lineEditStreams)
        self.label_5 = QtWidgets.QLabel(self.groupBox_2)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.lineEditReactions = QtWidgets.QLineEdit(self.groupBox_2)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.lineEditReactions.setFont(font)
        self.lineEditReactions.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEditReactions.setReadOnly(True)
        self.lineEditReactions.setObjectName("lineEditReactions")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.lineEditReactions)
        self.label_6 = QtWidgets.QLabel(self.groupBox_2)
        self.label_6.setObjectName("label_6")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.label_6)
        self.lineEditSensAnalysis = QtWidgets.QLineEdit(self.groupBox_2)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.lineEditSensAnalysis.setFont(font)
        self.lineEditSensAnalysis.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEditSensAnalysis.setReadOnly(True)
        self.lineEditSensAnalysis.setObjectName("lineEditSensAnalysis")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.lineEditSensAnalysis)
        self.label_7 = QtWidgets.QLabel(self.groupBox_2)
        self.label_7.setObjectName("label_7")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.label_7)
        self.lineEditCalculators = QtWidgets.QLineEdit(self.groupBox_2)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.lineEditCalculators.setFont(font)
        self.lineEditCalculators.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEditCalculators.setReadOnly(True)
        self.lineEditCalculators.setObjectName("lineEditCalculators")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.lineEditCalculators)
        self.label_8 = QtWidgets.QLabel(self.groupBox_2)
        self.label_8.setObjectName("label_8")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.label_8)
        self.label_9 = QtWidgets.QLabel(self.groupBox_2)
        self.label_9.setObjectName("label_9")
        self.formLayout.setWidget(8, QtWidgets.QFormLayout.LabelRole, self.label_9)
        self.lineEditOptimizations = QtWidgets.QLineEdit(self.groupBox_2)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.lineEditOptimizations.setFont(font)
        self.lineEditOptimizations.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEditOptimizations.setReadOnly(True)
        self.lineEditOptimizations.setObjectName("lineEditOptimizations")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.FieldRole, self.lineEditOptimizations)
        self.lineEditDesSpecs = QtWidgets.QLineEdit(self.groupBox_2)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.lineEditDesSpecs.setFont(font)
        self.lineEditDesSpecs.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEditDesSpecs.setReadOnly(True)
        self.lineEditDesSpecs.setObjectName("lineEditDesSpecs")
        self.formLayout.setWidget(8, QtWidgets.QFormLayout.FieldRole, self.lineEditDesSpecs)
        self.gridLayout_3.addLayout(self.formLayout, 1, 1, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.groupBox_2)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.gridLayout_3.addWidget(self.label_10, 3, 1, 1, 1)
        spacerItem7 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout_3.addItem(spacerItem7, 5, 1, 1, 1)
        self.label_14 = QtWidgets.QLabel(self.groupBox_2)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_14.setFont(font)
        self.label_14.setObjectName("label_14")
        self.gridLayout_3.addWidget(self.label_14, 0, 1, 1, 1)
        self.tableWidgetSimulationData = QtWidgets.QTableWidget(self.groupBox_2)
        self.tableWidgetSimulationData.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidgetSimulationData.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.tableWidgetSimulationData.setObjectName("tableWidgetSimulationData")
        self.tableWidgetSimulationData.setColumnCount(8)
        self.tableWidgetSimulationData.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidgetSimulationData.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidgetSimulationData.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidgetSimulationData.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidgetSimulationData.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidgetSimulationData.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidgetSimulationData.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidgetSimulationData.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidgetSimulationData.setHorizontalHeaderItem(7, item)
        self.tableWidgetSimulationData.horizontalHeader().setStretchLastSection(True)
        self.gridLayout_3.addWidget(self.tableWidgetSimulationData, 4, 1, 1, 1)
        self.gridLayout_6.addWidget(self.groupBox_2, 0, 1, 1, 1)
        self.groupBox_6 = QtWidgets.QGroupBox(self.simulationTab)
        self.groupBox_6.setStyleSheet("QGroupBox {\n"
"    border: 1px solid gray;\n"
"    border-radius: 9px;\n"
"    font-weight: bold;\n"
"}\n"
"\n"
"QGroupBox::title {\n"
"    subcontrol-origin: margin;\n"
"    left: 10px;\n"
"    top: 5px;\n"
"    padding: 0 3px 0 3px;\n"
"}")
        self.groupBox_6.setTitle("")
        self.groupBox_6.setObjectName("groupBox_6")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.groupBox_6)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.label_12 = QtWidgets.QLabel(self.groupBox_6)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_12.setFont(font)
        self.label_12.setObjectName("label_12")
        self.gridLayout_7.addWidget(self.label_12, 0, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem8 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem8)
        self.buttonAddExpr = QtWidgets.QPushButton(self.groupBox_6)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/loadsim/add_icon.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.buttonAddExpr.setIcon(icon)
        self.buttonAddExpr.setObjectName("buttonAddExpr")
        self.horizontalLayout_2.addWidget(self.buttonAddExpr)
        self.gridLayout_7.addLayout(self.horizontalLayout_2, 0, 1, 1, 1)
        self.tableWidgetExpressions = QtWidgets.QTableWidget(self.groupBox_6)
        self.tableWidgetExpressions.setEditTriggers(QtWidgets.QAbstractItemView.AllEditTriggers)
        self.tableWidgetExpressions.setObjectName("tableWidgetExpressions")
        self.tableWidgetExpressions.setColumnCount(3)
        self.tableWidgetExpressions.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidgetExpressions.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidgetExpressions.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidgetExpressions.setHorizontalHeaderItem(2, item)
        self.tableWidgetExpressions.horizontalHeader().setStretchLastSection(True)
        self.gridLayout_7.addWidget(self.tableWidgetExpressions, 1, 0, 1, 2)
        self.gridLayout_6.addWidget(self.groupBox_6, 1, 0, 1, 2)
        self.tabMainWidget.addTab(self.simulationTab, "")
        self.samplingTab = QtWidgets.QWidget()
        self.samplingTab.setEnabled(True)
        self.samplingTab.setObjectName("samplingTab")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.samplingTab)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.groupBox_3 = QtWidgets.QGroupBox(self.samplingTab)
        self.groupBox_3.setStyleSheet("QGroupBox {\n"
"    border: 1px solid gray;\n"
"    border-radius: 9px;\n"
"    font-weight: bold;\n"
"}\n"
"\n"
"QGroupBox::title {\n"
"    subcontrol-origin: margin;\n"
"    left: 10px;\n"
"    top: 5px;\n"
"    padding: 0 3px 0 3px;\n"
"}")
        self.groupBox_3.setTitle("")
        self.groupBox_3.setObjectName("groupBox_3")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.groupBox_3)
        self.gridLayout_5.setObjectName("gridLayout_5")
        spacerItem9 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_5.addItem(spacerItem9, 1, 0, 1, 1)
        spacerItem10 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout_5.addItem(spacerItem10, 2, 1, 1, 1)
        self.radioButton = QtWidgets.QRadioButton(self.groupBox_3)
        self.radioButton.setChecked(False)
        self.radioButton.setObjectName("radioButton")
        self.gridLayout_5.addWidget(self.radioButton, 1, 1, 1, 1)
        self.radioButton_2 = QtWidgets.QRadioButton(self.groupBox_3)
        self.radioButton_2.setChecked(True)
        self.radioButton_2.setObjectName("radioButton_2")
        self.gridLayout_5.addWidget(self.radioButton_2, 3, 1, 1, 1)
        spacerItem11 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        self.gridLayout_5.addItem(spacerItem11, 4, 1, 1, 1)
        self.groupBox_5 = QtWidgets.QGroupBox(self.groupBox_3)
        self.groupBox_5.setEnabled(False)
        self.groupBox_5.setTitle("")
        self.groupBox_5.setObjectName("groupBox_5")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox_5)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tableWidget_2 = QtWidgets.QTableWidget(self.groupBox_5)
        self.tableWidget_2.setObjectName("tableWidget_2")
        self.tableWidget_2.setColumnCount(3)
        self.tableWidget_2.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(2, item)
        self.tableWidget_2.horizontalHeader().setStretchLastSection(True)
        self.horizontalLayout.addWidget(self.tableWidget_2)
        self.pushButton = QtWidgets.QPushButton(self.groupBox_5)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(self.groupBox_5)
        self.pushButton_2.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/sampling/settings_icon.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_2.setIcon(icon1)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.gridLayout_5.addWidget(self.groupBox_5, 1, 2, 1, 2)
        self.groupBox_7 = QtWidgets.QGroupBox(self.groupBox_3)
        self.groupBox_7.setTitle("")
        self.groupBox_7.setObjectName("groupBox_7")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.groupBox_7)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.lineEdit = QtWidgets.QLineEdit(self.groupBox_7)
        self.lineEdit.setReadOnly(True)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout_3.addWidget(self.lineEdit)
        self.pushButton_3 = QtWidgets.QPushButton(self.groupBox_7)
        self.pushButton_3.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/sampling/open_icon.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_3.setIcon(icon2)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout_3.addWidget(self.pushButton_3)
        self.pushButton_4 = QtWidgets.QPushButton(self.groupBox_7)
        self.pushButton_4.setObjectName("pushButton_4")
        self.horizontalLayout_3.addWidget(self.pushButton_4)
        self.gridLayout_5.addWidget(self.groupBox_7, 3, 2, 1, 2)
        self.label_15 = QtWidgets.QLabel(self.groupBox_3)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_15.setFont(font)
        self.label_15.setObjectName("label_15")
        self.gridLayout_5.addWidget(self.label_15, 0, 1, 1, 1)
        self.gridLayout_2.addWidget(self.groupBox_3, 0, 0, 1, 1)
        self.groupBox_4 = QtWidgets.QGroupBox(self.samplingTab)
        self.groupBox_4.setStyleSheet("QGroupBox {\n"
"    border: 1px solid gray;\n"
"    border-radius: 9px;\n"
"    font-weight: bold;\n"
"}\n"
"\n"
"QGroupBox::title {\n"
"    subcontrol-origin: margin;\n"
"    left: 10px;\n"
"    top: 5px;\n"
"    padding: 0 3px 0 3px;\n"
"}")
        self.groupBox_4.setTitle("")
        self.groupBox_4.setObjectName("groupBox_4")
        self.gridLayout_8 = QtWidgets.QGridLayout(self.groupBox_4)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.tableWidget = QtWidgets.QTableWidget(self.groupBox_4)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.gridLayout_8.addWidget(self.tableWidget, 1, 0, 1, 1)
        self.label_16 = QtWidgets.QLabel(self.groupBox_4)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_16.setFont(font)
        self.label_16.setObjectName("label_16")
        self.gridLayout_8.addWidget(self.label_16, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.groupBox_4, 2, 0, 1, 1)
        spacerItem12 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout_2.addItem(spacerItem12, 1, 0, 1, 1)
        self.tabMainWidget.addTab(self.samplingTab, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setEnabled(True)
        self.tab_3.setObjectName("tab_3")
        self.tabMainWidget.addTab(self.tab_3, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setEnabled(True)
        self.tab_4.setObjectName("tab_4")
        self.tabMainWidget.addTab(self.tab_4, "")
        self.tab_5 = QtWidgets.QWidget()
        self.tab_5.setEnabled(True)
        self.tab_5.setObjectName("tab_5")
        self.tabMainWidget.addTab(self.tab_5, "")
        self.gridLayout_4.addWidget(self.tabMainWidget, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1026, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpenSimFile = QtWidgets.QAction(MainWindow)
        self.actionOpenSimFile.setObjectName("actionOpenSimFile")
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        self.tabMainWidget.setCurrentIndex(0)
        self.radioButton.toggled['bool'].connect(self.groupBox_5.setEnabled)
        self.radioButton_2.toggled['bool'].connect(self.groupBox_7.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.tabMainWidget, self.textBrowserSimFile)
        MainWindow.setTabOrder(self.textBrowserSimFile, self.buttonOpenSimFile)
        MainWindow.setTabOrder(self.buttonOpenSimFile, self.buttonLoadVariables)
        MainWindow.setTabOrder(self.buttonLoadVariables, self.lineEditComponents)
        MainWindow.setTabOrder(self.lineEditComponents, self.lineEditMethodName)
        MainWindow.setTabOrder(self.lineEditMethodName, self.lineEditBlocks)
        MainWindow.setTabOrder(self.lineEditBlocks, self.lineEditStreams)
        MainWindow.setTabOrder(self.lineEditStreams, self.lineEditReactions)
        MainWindow.setTabOrder(self.lineEditReactions, self.lineEditSensAnalysis)
        MainWindow.setTabOrder(self.lineEditSensAnalysis, self.lineEditCalculators)
        MainWindow.setTabOrder(self.lineEditCalculators, self.lineEditOptimizations)
        MainWindow.setTabOrder(self.lineEditOptimizations, self.lineEditDesSpecs)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.buttonOpenSimFile.setToolTip(_translate("MainWindow", "Opens a file prompt to select an Aspen .bkp simulation file."))
        self.buttonOpenSimFile.setText(_translate("MainWindow", "Open File"))
        self.buttonLoadVariables.setToolTip(_translate("MainWindow", "Opens a window that allows variable selection from the simulation file."))
        self.buttonLoadVariables.setText(_translate("MainWindow", "Load Variables"))
        self.tableWidgetAliasDisplay.setSortingEnabled(True)
        item = self.tableWidgetAliasDisplay.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Alias"))
        item = self.tableWidgetAliasDisplay.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Type"))
        self.textBrowserSimFile.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Select a simulation file.</span></p></body></html>"))
        self.label_13.setText(_translate("MainWindow", "Load Simulation File"))
        self.label_11.setText(_translate("MainWindow", "Selected variables aliases"))
        self.label.setText(_translate("MainWindow", "No. components:"))
        self.label_2.setText(_translate("MainWindow", "Thermodynamic model:"))
        self.label_3.setText(_translate("MainWindow", "No. Blocks:"))
        self.label_4.setText(_translate("MainWindow", "No.Streams:"))
        self.label_5.setText(_translate("MainWindow", "No. Reactions:"))
        self.label_6.setText(_translate("MainWindow", "No. Sensitivity Analysis:"))
        self.label_7.setText(_translate("MainWindow", "No. Calculators:"))
        self.label_8.setText(_translate("MainWindow", "No. Optimizations:"))
        self.label_9.setText(_translate("MainWindow", "No. Design Specs:"))
        self.label_10.setText(_translate("MainWindow", "Description Info"))
        self.label_14.setText(_translate("MainWindow", "Simulation Info"))
        item = self.tableWidgetSimulationData.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Components"))
        item = self.tableWidgetSimulationData.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Blocks"))
        item = self.tableWidgetSimulationData.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Streams"))
        item = self.tableWidgetSimulationData.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Reactions"))
        item = self.tableWidgetSimulationData.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Sensitivity"))
        item = self.tableWidgetSimulationData.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "Calculators"))
        item = self.tableWidgetSimulationData.horizontalHeaderItem(6)
        item.setText(_translate("MainWindow", "Optimizations"))
        item = self.tableWidgetSimulationData.horizontalHeaderItem(7)
        item.setText(_translate("MainWindow", "Design Specs"))
        self.label_12.setText(_translate("MainWindow", "Functions definitions"))
        self.buttonAddExpr.setToolTip(_translate("MainWindow", "<html><head/><body><p>Inserts a new expression slot</p></body></html>"))
        self.buttonAddExpr.setText(_translate("MainWindow", "Add Expression"))
        item = self.tableWidgetExpressions.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Name"))
        item = self.tableWidgetExpressions.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Expression"))
        item = self.tableWidgetExpressions.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Type"))
        self.tabMainWidget.setTabText(self.tabMainWidget.indexOf(self.simulationTab), _translate("MainWindow", "Load Simulation"))
        self.radioButton.setText(_translate("MainWindow", "Set LHS inputs:"))
        self.radioButton_2.setText(_translate("MainWindow", "Load data from CSV file:"))
        item = self.tableWidget_2.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Variable"))
        item = self.tableWidget_2.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Lower bound"))
        item = self.tableWidget_2.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Upper bound"))
        self.pushButton.setText(_translate("MainWindow", "Generate LHS"))
        self.pushButton_2.setToolTip(_translate("MainWindow", "<html><head/><body><p>Latin Hypercube Sampling (LHS) settings</p></body></html>"))
        self.pushButton_3.setToolTip(_translate("MainWindow", "<html><head/><body><p>Select .csv file to extract the data from</p></body></html>"))
        self.pushButton_4.setText(_translate("MainWindow", "CSV editor"))
        self.label_15.setText(_translate("MainWindow", "Design of Experiments (DOE) Settings"))
        self.label_16.setText(_translate("MainWindow", "DOE Results"))
        self.tabMainWidget.setTabText(self.tabMainWidget.indexOf(self.samplingTab), _translate("MainWindow", "Sampling"))
        self.tabMainWidget.setTabText(self.tabMainWidget.indexOf(self.tab_3), _translate("MainWindow", "Page"))
        self.tabMainWidget.setTabText(self.tabMainWidget.indexOf(self.tab_4), _translate("MainWindow", "Page"))
        self.tabMainWidget.setTabText(self.tabMainWidget.indexOf(self.tab_5), _translate("MainWindow", "Page"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionOpenSimFile.setText(_translate("MainWindow", "openSimFile"))

from gui.resources import icons_rc
