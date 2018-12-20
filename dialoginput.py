# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialoginput.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DialogInput(object):
    def setupUi(self, DialogInput):
        DialogInput.setObjectName("DialogInput")
        DialogInput.resize(624, 337)
        self.label_Name = QtWidgets.QLabel(DialogInput)
        self.label_Name.setGeometry(QtCore.QRect(20, 60, 61, 21))
        self.label_Name.setObjectName("label_Name")
        self.lineEdit_Name = QtWidgets.QLineEdit(DialogInput)
        self.lineEdit_Name.setGeometry(QtCore.QRect(150, 60, 301, 21))
        self.lineEdit_Name.setText("")
        self.lineEdit_Name.setReadOnly(True)
        self.lineEdit_Name.setObjectName("lineEdit_Name")
        self.label_2 = QtWidgets.QLabel(DialogInput)
        self.label_2.setGeometry(QtCore.QRect(20, 100, 81, 21))
        self.label_2.setObjectName("label_2")
        self.lineEdit_Designation = QtWidgets.QLineEdit(DialogInput)
        self.lineEdit_Designation.setGeometry(QtCore.QRect(150, 100, 301, 21))
        self.lineEdit_Designation.setReadOnly(True)
        self.lineEdit_Designation.setObjectName("lineEdit_Designation")
        self.label_3 = QtWidgets.QLabel(DialogInput)
        self.label_3.setGeometry(QtCore.QRect(20, 140, 121, 21))
        self.label_3.setObjectName("label_3")
        self.lineEdit_PathToDraw = QtWidgets.QLineEdit(DialogInput)
        self.lineEdit_PathToDraw.setGeometry(QtCore.QRect(150, 140, 301, 21))
        self.lineEdit_PathToDraw.setReadOnly(True)
        self.lineEdit_PathToDraw.setObjectName("lineEdit_PathToDraw")
        self.label_4 = QtWidgets.QLabel(DialogInput)
        self.label_4.setGeometry(QtCore.QRect(20, 180, 121, 21))
        self.label_4.setObjectName("label_4")
        self.lineEdit_PathToModel = QtWidgets.QLineEdit(DialogInput)
        self.lineEdit_PathToModel.setGeometry(QtCore.QRect(150, 180, 301, 21))
        self.lineEdit_PathToModel.setReadOnly(True)
        self.lineEdit_PathToModel.setObjectName("lineEdit_PathToModel")
        self.toolButton_Draw = QtWidgets.QToolButton(DialogInput)
        self.toolButton_Draw.setEnabled(False)
        self.toolButton_Draw.setGeometry(QtCore.QRect(460, 140, 28, 21))
        self.toolButton_Draw.setObjectName("toolButton_Draw")
        self.toolButton_Model = QtWidgets.QToolButton(DialogInput)
        self.toolButton_Model.setEnabled(False)
        self.toolButton_Model.setGeometry(QtCore.QRect(460, 180, 28, 21))
        self.toolButton_Model.setObjectName("toolButton_Model")
        self.Cancel_Button = QtWidgets.QPushButton(DialogInput)
        self.Cancel_Button.setGeometry(QtCore.QRect(400, 251, 91, 41))
        self.Cancel_Button.setObjectName("Cancel_Button")
        self.OKButton = QtWidgets.QPushButton(DialogInput)
        self.OKButton.setGeometry(QtCore.QRect(279, 251, 91, 41))
        self.OKButton.setObjectName("OKButton")
        self.Edit_Button = QtWidgets.QPushButton(DialogInput)
        self.Edit_Button.setGeometry(QtCore.QRect(419, 11, 81, 31))
        self.Edit_Button.setObjectName("Edit_Button")

        self.retranslateUi(DialogInput)
        QtCore.QMetaObject.connectSlotsByName(DialogInput)

    def retranslateUi(self, DialogInput):
        _translate = QtCore.QCoreApplication.translate
        DialogInput.setWindowTitle(_translate("DialogInput", "Dialog"))
        self.label_Name.setText(_translate("DialogInput", "Name"))
        self.label_2.setText(_translate("DialogInput", "Designation"))
        self.label_3.setText(_translate("DialogInput", "Path to drawing"))
        self.lineEdit_PathToDraw.setText(_translate("DialogInput", "Path to drawing"))
        self.label_4.setText(_translate("DialogInput", "Path to 3d-model"))
        self.lineEdit_PathToModel.setText(_translate("DialogInput", "Path to 3d model"))
        self.toolButton_Draw.setText(_translate("DialogInput", "..."))
        self.toolButton_Model.setText(_translate("DialogInput", "..."))
        self.Cancel_Button.setText(_translate("DialogInput", "Cancel"))
        self.OKButton.setText(_translate("DialogInput", "OK"))
        self.Edit_Button.setText(_translate("DialogInput", "Edit"))

