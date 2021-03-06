import json
import sys  # sys нужен для передачи argv в QApplication
import os
import threading

from PyQt5 import QtWidgets
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QFileDialog, QSizePolicy

import design  # конвертированный файл дизайна
import dialoginput


from pdf2image import convert_from_path
import requests


class InputDialog(QtWidgets.QDialog, dialoginput.Ui_DialogInput):
    def __init__(self, tableWidget):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Dialog input part")

        self.Edit_Button.clicked.connect(self.edit)

        self.toolButton_Model.clicked.connect(self.showDialog)
        self.toolButton_Draw.clicked.connect(self.showDialog)

        self.OKButton.clicked.connect(self.sendTobase)
        self.Cancel_Button.clicked.connect(self.close)

        self.tableWidget = tableWidget
        self.id = None

    def show_data(self, name, designation,information, model_id, draw_id, id=None):
        self.id = id
        print(id)
        self.lineEdit_Name.setText(name)
        self.lineEdit_Designation.setText(designation)
        self.lineEdit_Information.setText(information)
        self.lineEdit_PathToModel.setText(model_id)
        self.lineEdit_PathToDraw.setText(draw_id)
        # self.OKButton.setEnabled(False)

    def edit(self):
        self.editlabel = True
        self.lineEdit_Name.setReadOnly(False)
        self.lineEdit_Designation.setReadOnly(False)
        self.toolButton_Draw.setEnabled(True)
        self.toolButton_Model.setEnabled(True)
        self.OKButton.setEnabled(True)

    def showDialog(self):

        sender = self.sender()
        if sender.objectName() == "toolButton_Model":
            fname = QFileDialog.getOpenFileName(self, 'Open file', '/home', 'STL (*.stl)')[0]
            self.lineEdit_PathToModel.setText(fname)
        elif sender.objectName() == "toolButton_Draw":
            fname = QFileDialog.getOpenFileName(self, 'Open file', '/home', 'PDF (*.PDF *.pdf)')[0]
            self.lineEdit_PathToDraw.setText(fname)

    def sendTobase(self):

        name = self.lineEdit_Name.text()
        designation = self.lineEdit_Designation.text()
        information=self.lineEdit_Information.text()
        model_id = self.lineEdit_PathToModel.text()
        draw_id = self.lineEdit_PathToDraw.text()

        MainApp.sendTobase(self, name, designation, information, model_id, draw_id, self.id)

        self.lineEdit_Name.clear()
        self.lineEdit_Designation.clear()
        self.lineEdit_PathToDraw.clear()
        self.lineEdit_PathToModel.clear()
        self.lineEdit_Information.clear()


class MainApp(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.createTable()


        # self.deleteSelected.clicked.connect(self.delete_doc)  # Выполнить функцию
        self.showDB()
        self.AddButton.clicked.connect(self.showInputDialog)  # Выполнить функцию
        self.EditButton.clicked.connect(self.showInputDialog)  # Выполнить функцию
        # self.ConnectButton.clicked.connect(self.connect)
        self.ExitButton.clicked.connect(self.close)
        self.DeleteButton.clicked.connect(self.delete_doc)  # Выполнить функцию

        self.tableWidget.doubleClicked.connect(self.showInputDialog)

    def thread(func):
        def wrapper(*args, **kwargs):
            my_thread = threading.Thread(target=func, args=args, kwargs=kwargs)
            my_thread.start()

        return wrapper

    def showDB(self):
        try:
            self.data = requests.get('http://192.168.1.4:5000/show_db',timeout= 1).json()
        except TimeoutError as err:
            self.statusBar.showMessage("1")

        count = len(self.data["cursor"])
        self.tableWidget.setRowCount(count)

        for doc, i in zip(self.data["cursor"], range(count)):
            print(doc)
            print(i)
            print(str(doc['_id']['$oid']))
            self.tableWidget.setItem(i, 0, QTableWidgetItem(str(doc['_id']['$oid'])))
            self.tableWidget.setItem(i, 1, QTableWidgetItem(str(doc["Name"])))
            self.tableWidget.setItem(i, 2, QTableWidgetItem(str(doc['Designation'])))
            self.tableWidget.setItem(i, 3, QTableWidgetItem( str(doc['information'])))
            self.tableWidget.setItem(i, 4, QTableWidgetItem(str(doc['Draw_img'])))
            self.tableWidget.setItem(i, 5, QTableWidgetItem(str(doc['3d_model'])))
            self.tableWidget.setItem(i, 6, QTableWidgetItem(str(doc['draw_id_img'])))
            self.tableWidget.setItem(i, 7, QTableWidgetItem(str(doc['draw_id_img_preview'])))


    def createTable(self):
        # Create table


        self.tableWidget.setColumnCount(8)
        self.tableWidget.setHorizontalHeaderLabels(
            ["id", "Name", "Designation", "Infomation","Draw_img", "3d_model", 'draw_id_img', 'draw_id_img_preview'])
        self.tableWidget.setColumnWidth(3,500)
        # self.tableWidget.font()
        # self.tableWidget.move(0, 0)

    def delete_doc(self):
        try:

            id = self.tableWidget.selectedItems()[0].text()
            print(id)
            requests.post('http://192.168.1.4:5000/get_image', json={"id": str(id)})

            self.showDB()
        except IndexError as err:
            self.statusBar.showMessage("Error: Choose a row for delete")
        self.statusBar.showMessage("Doc deleted")

    def showInputDialog(self):
        sender = self.sender()

        win = InputDialog(self.tableWidget)

        print(sender.objectName())
        if sender.objectName() == "EditButton" or sender.objectName() == "tableWidget":

            if sender.objectName() == "EditButton":
                win.edit()
                win.Edit_Button.setVisible(False)
                win.OKButton.setEnabled(True)
            else:
                win.Edit_Button.setVisible(True)
                win.OKButton.setEnabled(False)

            win.show_data(self.tableWidget.selectedItems()[1].text(), self.tableWidget.selectedItems()[2].text(),
                          self.tableWidget.selectedItems()[3].text(), self.tableWidget.selectedItems()[4].text(),
                          self.tableWidget.selectedItems()[5].text(),self.tableWidget.selectedItems()[0].text())

        elif sender.objectName() == "AddButton":
            win.edit()
            win.Edit_Button.setVisible(False)

        win.exec()

    @thread
    def sendTobase(self, name, designation, information,path_model, path_draw, id):
        print(id)

        def pdfToimg(pdf_path):
            pages = convert_from_path(pdf_path, 200)
            pages[0].save('/home/oleg/PycharmProjects/QT/tmp/out.jpg', 'JPEG')
            pages = convert_from_path(pdf_path, 10)
            pages[0].save('/home/oleg/PycharmProjects/QT/tmp/out2.jpg', 'JPEG')
            
        if path_draw.startswith('/'):
            pdfToimg(path_draw)

        data = {'file_model': (os.path.basename(path_model), open(path_model, 'rb'), 'application/octet-stream'),
                'file_draw': (os.path.basename(path_draw), open(path_draw, 'rb'), 'application/octet-stream'),
                'draw_img': (os.path.basename('/home/oleg/PycharmProjects/QT/tmp/out.jpg'),
                             open('/home/oleg/PycharmProjects/QT/tmp/out.jpg', 'rb'), 'application/octet-stream'),
                'draw_img_preview': (os.path.basename('/home/oleg/PycharmProjects/QT/tmp/out2.jpg'),
                                     open('/home/oleg/PycharmProjects/QT/tmp/out2.jpg', 'rb'),
                                     'application/octet-stream'),
                'data': ('data', json.dumps(dict({'name': name, 'designation': designation,'information':information})), 'application/json'),
                }
        requests.post('http://192.168.1.4:5000/add_part', files=data)

        self.showDB()
        self.statusBar.showMessage("New part has been added")


def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication

    window = MainApp()  # Создаём объект класса ExampleApp
    dialog = QtWidgets.QDialog
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()
