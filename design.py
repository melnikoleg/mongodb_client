# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(841, 612)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.AddButton = QtWidgets.QPushButton(self.centralWidget)
        self.AddButton.setGeometry(QtCore.QRect(40, 30, 101, 41))
        self.AddButton.setObjectName("AddButton")
        self.DeleteButton = QtWidgets.QPushButton(self.centralWidget)
        self.DeleteButton.setGeometry(QtCore.QRect(160, 30, 101, 41))
        self.DeleteButton.setObjectName("DeleteButton")
        self.EditButton = QtWidgets.QPushButton(self.centralWidget)
        self.EditButton.setGeometry(QtCore.QRect(280, 30, 101, 41))
        self.EditButton.setObjectName("EditButton")
        self.ConnectButton = QtWidgets.QPushButton(self.centralWidget)
        self.ConnectButton.setGeometry(QtCore.QRect(710, 50, 101, 41))
        self.ConnectButton.setObjectName("ConnectButton")
        self.tableWidget = QtWidgets.QTableWidget(self.centralWidget)
        self.tableWidget.setGeometry(QtCore.QRect(20, 170, 791, 381))
        self.tableWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tableWidget.setMidLineWidth(-1)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.comboBox = QtWidgets.QComboBox(self.centralWidget)
        self.comboBox.setGeometry(QtCore.QRect(670, 20, 141, 22))
        self.comboBox.setMaximumSize(QtCore.QSize(141, 16777215))
        font = QtGui.QFont()
        font.setKerning(False)
        self.comboBox.setFont(font)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.ExitButton = QtWidgets.QPushButton(self.centralWidget)
        self.ExitButton.setGeometry(QtCore.QRect(710, 110, 101, 41))
        self.ExitButton.setObjectName("ExitButton")
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 841, 19))
        self.menuBar.setObjectName("menuBar")
        MainWindow.setMenuBar(self.menuBar)
        self.mainToolBar = QtWidgets.QToolBar(MainWindow)
        self.mainToolBar.setObjectName("mainToolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.mainToolBar.addSeparator()

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.AddButton.setText(_translate("MainWindow", "Add"))
        self.DeleteButton.setText(_translate("MainWindow", "Delete"))
        self.EditButton.setText(_translate("MainWindow", "Edit"))
        self.ConnectButton.setText(_translate("MainWindow", "Connect"))
        self.comboBox.setItemText(0, _translate("MainWindow", "192.168.1.229"))
        self.comboBox.setItemText(1, _translate("MainWindow", "localhost"))
        self.comboBox.setItemText(2, _translate("MainWindow", "192.168.1.242"))
        self.ExitButton.setText(_translate("MainWindow", "Exit"))

