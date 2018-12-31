import sys  # sys нужен для передачи argv в QApplication
import os
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QFileDialog, QMainWindow, QApplication, QDialog, QComboBox
from pymongo import MongoClient
from pymongo import errors
import design  # конвертированный файл дизайна
import dialoginput
import gridfs
from bson.objectid import ObjectId
from pdf2image import convert_from_path


class InputDialog(QtWidgets.QDialog, dialoginput.Ui_DialogInput):
    def __init__(self, db, coll, tableWidget):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Dialog input part")

        self.Edit_Button.clicked.connect(self.edit)

        self.toolButton_Model.clicked.connect(self.showDialog)
        self.toolButton_Draw.clicked.connect(self.showDialog)

        self.OKButton.clicked.connect(self.sendTobase)
        self.Cancel_Button.clicked.connect(self.close)

        self.db = db
        self.coll = coll
        self.tableWidget = tableWidget
        self.id = None

    def show_data(self, name, designation, model_id, draw_id, id=None):
        self.id = id

        self.lineEdit_Name.setText(name)
        self.lineEdit_Designation.setText(designation)

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

        model_id = self.lineEdit_PathToModel.text()
        draw_id = self.lineEdit_PathToDraw.text()

        MainApp.sendTobase(self, name, designation, model_id, draw_id, self.id)

        self.lineEdit_Name.clear()
        self.lineEdit_Designation.clear()
        self.lineEdit_PathToDraw.clear()
        self.lineEdit_PathToModel.clear()


class MainApp(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.createTable()

        # self.deleteSelected.clicked.connect(self.delete_doc)  # Выполнить функцию

        self.AddButton.clicked.connect(self.showInputDialog)  # Выполнить функцию
        self.EditButton.clicked.connect(self.showInputDialog)  # Выполнить функцию
        self.ConnectButton.clicked.connect(self.connect)
        self.ExitButton.clicked.connect(self.close)
        self.DeleteButton.clicked.connect(self.delete_doc)  # Выполнить функцию

        self.tableWidget.doubleClicked.connect(self.showInputDialog)

    def connect(self):
        var = self.comboBox.currentText()
        try:
            self.conn = MongoClient(host=var, port=27017, serverSelectionTimeoutMS=1)
            self.conn.server_info()

            self.db = self.conn["Parts"]
            self.coll = self.db["Part"]
            self.showDB()
            self.statusBar.showMessage("Connected")
        except errors.ServerSelectionTimeoutError as err:
            # do whatever you need
            self.statusBar.showMessage(str(err))

    def showDB(self):
        self.tableWidget.setRowCount(self.coll.count())
        for doc, i in zip(self.coll.find(), range(self.coll.count())):
            # print(i)
            self.tableWidget.setItem(i, 0, QTableWidgetItem(str(doc['_id'])))
            self.tableWidget.setItem(i, 1, QTableWidgetItem(str(doc['Name'])))
            self.tableWidget.setItem(i, 2, QTableWidgetItem(str(doc['Designation'])))
            self.tableWidget.setItem(i, 3, QTableWidgetItem(str(doc['Draw_img'])))
            self.tableWidget.setItem(i, 4, QTableWidgetItem(str(doc['3d_model'])))
            self.tableWidget.setItem(i, 5, QTableWidgetItem(str(doc['draw_id_img'])))
            self.tableWidget.setItem(i, 6, QTableWidgetItem(str(doc['draw_id_img_preview'])))

    def createTable(self):
        # Create table
        self.tableWidget = self.tableWidget

        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels(
            ["id", "Name", "Designation", "Draw_img", "3d_model", 'draw_id_img', 'draw_id_img_preview'])

        # self.tableWidget.font()
        # self.tableWidget.move(0, 0)

    def delete_doc(self):
        try:

            id = self.tableWidget.selectedItems()[0].text()
            # print(id)
            self.coll.remove({'_id': ObjectId(id)})
            self.showDB()
        except IndexError as err:
            self.statusBar.showMessage("Error: Choose a row for delete")
        self.statusBar.showMessage("Doc deleted")

    def showInputDialog(self):
        sender = self.sender()

        win = InputDialog(self.db, self.coll, self.tableWidget)

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
                          self.tableWidget.selectedItems()[0].text())

        elif sender.objectName() == "AddButton":
            win.edit()
            win.Edit_Button.setVisible(False)

        win.exec()

    def sendTobase(self, name, designation, path_model, path_draw, id):
        print(id)

        fss = gridfs.GridFSBucket(self.db)

        def upload_to_gridfs(path):
            try:
                with open(path, 'rb') as f:
                    file_id = fss.upload_from_stream(os.path.split(path)[-1], f.read())

                return file_id
            except FileNotFoundError as err:
                self.statusBar.showMessage("No file selected")

        def pdfToimg(pdf_path):
            pages = convert_from_path(pdf_path, 200)
            pages[0].save('/home/oleg/PycharmProjects/QT/tmp/out.jpg', 'JPEG')
            pages = convert_from_path(pdf_path, 10)
            pages[0].save('/home/oleg/PycharmProjects/QT/tmp/out2.jpg', 'JPEG')

        if path_draw.startswith('/'):

            pdfToimg(path_draw)

            draw_id = upload_to_gridfs(path_draw)
            draw_id_img = upload_to_gridfs("/home/oleg/PycharmProjects/QT/tmp/out.jpg")
            draw_id_img_preview = upload_to_gridfs("/home/oleg/PycharmProjects/QT/tmp/out2.jpg")

            if id != None:
                self.coll.update({'_id': id}, {'$set': {'Draw_img': str(draw_id), 'draw_id_img': str(draw_id_img),
                                                        'draw_id_img_preview': draw_id_img_preview}})

        if path_model.startswith('/'):
            model_id = upload_to_gridfs(path_model)
            if id != None:
                self.coll.update({'_id': id}, {'$set': {'3d_model': str(model_id)}})

        if id == None:
            self.coll.insert(
                {'Name': str(name), '3d_model': str(model_id), 'Designation': str(designation),
                 'Draw_img': str(draw_id),
                 'draw_id_img': str(draw_id_img), 'draw_id_img_preview': draw_id_img_preview})

        else:
            self.coll.update({'_id': ObjectId(id)}, {'$set': {'Name': str(name), 'Designation': str(designation)}})

        MainApp.showDB(self)


def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication

    window = MainApp()  # Создаём объект класса ExampleApp
    dialog = QtWidgets.QDialog
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()
