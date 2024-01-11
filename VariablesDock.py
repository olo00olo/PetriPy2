from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QDockWidget, QVBoxLayout, QWidget, QPushButton, QTableWidgetItem, QTableWidget, \
    QComboBox, QLineEdit, QMessageBox
from PyQt5.uic.properties import QtGui


class VariablesDock(QDockWidget):
    def __init__(self, mainWindow, graphWidget):
        super().__init__()

        self.setWindowTitle("variables")
        self.setMinimumWidth(250)

        self.mainWindow = mainWindow
        self.graphWidget = graphWidget

        self.init_ui()

        self.varDict = {}
        self.userVarDict = {}

        self.uVar = {}

    def init_ui(self):
        dock_widget_content = QWidget(self)
        dock_widget_layout = QVBoxLayout(dock_widget_content)

        self.table_widget = QTableWidget(self)
        self.table_widget.setColumnCount(3)
        # self.table_widget.setHorizontalHeaderLabels(["Column 1", "Column 2", "Column 3"])
        self.table_widget.horizontalHeader().setVisible(False)

        self.table_widget.setColumnWidth(1, 55)  # Szerokość drugiej kolumny
        self.table_widget.setColumnWidth(2, 50)


        button = QPushButton("Click me!", self)
        button.clicked.connect(self.add_row)

        dock_widget_layout.addWidget(self.table_widget)
        dock_widget_layout.addWidget(button)

        self.setWidget(dock_widget_content)

    def add_row(self):
        row_position = self.table_widget.rowCount()

        if row_position > 0:
            if self.table_widget.cellWidget(row_position - 1, 0).text() == "temp":
                msgBox = QMessageBox()
                msgBox.information(self, "Information", "First change default variable")
                return


        self.table_widget.insertRow(row_position)

        item1 = QTableWidgetItem("")
        self.table_widget.setItem(row_position, 0, item1)
        line_edit = QLineEdit(self)
        line_edit.setText("temp")
        self.table_widget.setCellWidget(row_position, 0, line_edit)
        line_edit.editingFinished.connect(lambda: self.user_var(line_edit, item1))

        self.uVar.update({line_edit: "temp"})
        self.userVarDict.update({"temp": False})



        combo_box = QComboBox(self)
        combo_box.addItems(["False", "True"])
        self.table_widget.setCellWidget(row_position, 1, combo_box)
        combo_box.currentIndexChanged.connect(lambda index: self.user_var(combo_box, item1))


        remove_button = QPushButton("", self)
        remove_button.setIcon(QIcon("./icons/bin.png"))
        remove_button.clicked.connect(lambda _, row=row_position: self.remove_row(row))
        self.table_widget.setCellWidget(row_position, 2, remove_button)

    # def remove_and_call(self, row):
    #     print(self.table_widget.cellWidget(row, 0).text(), "co")
    #     self.remove_row(row)



    def user_var(self, widget, item):
        if isinstance(widget, QComboBox):
            k = self.table_widget.cellWidget(item.row(), 0).text()
            if widget.currentText() == "True":
                self.userVarDict.update({k: True})
            else:
                self.userVarDict.update({k: False})

            print(self.userVarDict, "dict")
        else:
            temp = self.table_widget.cellWidget(item.row(), 0).text()
            for key, value in self.graphWidget.placesDict.items():
                if temp in value.variables:
                    msgBox = QMessageBox()
                    msgBox.information(self, "Information", "Variable already exists")
                    return

            a = self.table_widget.cellWidget(item.row(), 0)
            for key, value in self.graphWidget.transitionsDict.items():
                sp = value.variables.split()
                print(sp, self.uVar[a])
                for x in range(len(sp)):
                    if x % 2 == 0:
                        print(sp[x])
                        print(self.uVar[a])
                        if sp[x][0] == "~":
                            if self.uVar[a] == sp[x][1:]:
                                msgBox = QMessageBox()
                                msgBox.information(self, "Information", "Variable connected to transition")
                                return
                        elif sp[x] == self.uVar[a]:
                            msgBox = QMessageBox()
                            msgBox.information(self, "Information", "Variable connected to transition")
                            return

            for x in range(self.table_widget.rowCount()):
                if self.table_widget.cellWidget(x, 0).text() == a.text() and item.row() != x:
                    msgBox = QMessageBox()
                    msgBox.information(self, "Information", "Variables duplicated")
                    return





            self.userVarDict[a.text()] = self.userVarDict[self.uVar[a]]
            del self.userVarDict[self.uVar[a]]

            self.uVar.update({a: a.text()})
        self.varDict.update(self.userVarDict)
        self.graphWidget.variableDict.update(self.varDict)



    # def value_changed(self, widget):
    #     if isinstance(widget, QComboBox):
    #         if widget.currentText() == "True":
    #             self.userVarDict.update({k: True})
    #         else:
    #             self.userVarDict.update({k: False})

    def remove_row(self, row):
        temp = self.table_widget.cellWidget(row, 0).text()



        for key, value in self.graphWidget.placesDict.items():
            if temp in value.variables:

                msgBox = QMessageBox()
                msgBox.information(self, "Information", "Variable is connected to P" + str(value.id))
                return

        for key, value in self.graphWidget.transitionsDict.items():
            sp = value.variables.split()
            for x in range(len(sp)):
                if x % 2 == 0:
                    if sp[x][0]== "~":
                        if temp == sp[x][1:]:
                            msgBox = QMessageBox()
                            msgBox.information(self, "Information", "Variable connected to transition")
                            return
                    elif sp[x] == temp:
                        msgBox = QMessageBox()
                        msgBox.information(self, "Information", "Variable connected to transition")
                        return


        if self.table_widget.cellWidget(row, 0).isEnabled():
            self.userVarDict.pop(temp)

        self.table_widget.removeRow(row)

        for r in range(self.table_widget.rowCount() - 1, -1, -1):
            remove_button = self.table_widget.cellWidget(r, 2)
            if remove_button:
                remove_button.clicked.disconnect()
                remove_button.clicked.connect(lambda _, row=r: self.remove_row(row))

    def populate_table(self):
        for key, value in self.varDict.items():
            row_position = self.table_widget.rowCount()
            self.table_widget.insertRow(row_position)

            item1 = QTableWidgetItem(str(key))
            self.table_widget.setItem(row_position, 0, item1)
            line_edit = QLineEdit(self)
            line_edit.setText(key)
            self.table_widget.setCellWidget(row_position, 0, line_edit)
            line_edit.editingFinished.connect(lambda: self.value_changed(item1))
            line_edit.setEnabled(False)
            line_edit.setStyleSheet("QLineEdit:disabled { color: black; }")

            combo_box = QComboBox(self)
            combo_box.addItems(["False", "True"])
            self.table_widget.setCellWidget(row_position, 1, combo_box)

            if value == True:
                combo_box.setCurrentIndex(0)
            else:
                print(self.userVarDict, "user22")
                combo_box.setCurrentIndex(1)
                print(self.userVarDict, "user221")
            combo_box.currentIndexChanged.connect(lambda index: self.user_var(combo_box, item1))

            # Dodaj przycisk usuwający do trzeciej kolumny
            remove_button = QPushButton("", self)
            remove_button.setIcon(QIcon("./icons/bin.png"))
            remove_button.clicked.connect(lambda _, row=row_position: self.remove_row(row))
            self.table_widget.setCellWidget(row_position, 2, remove_button)

        for key, value in self.userVarDict.items():
            print(self.userVarDict, "user")
            row_position = self.table_widget.rowCount()
            self.table_widget.insertRow(row_position)

            item1 = QTableWidgetItem(str(key))
            self.table_widget.setItem(row_position, 0, item1)
            line_edit = QLineEdit(self)
            line_edit.setText(key)
            self.table_widget.setCellWidget(row_position, 0, line_edit)
            line_edit.editingFinished.connect(lambda: lambda: self.user_var(line_edit, item1))
            # line_edit.setEnabled(False)
            # line_edit.setStyleSheet("QLineEdit:disabled { color: black; }")

            combo_box = QComboBox(self)
            combo_box.addItems(["False", "True"])
            self.table_widget.setCellWidget(row_position, 1, combo_box)
            combo_box.currentIndexChanged.connect(lambda index: self.user_var(combo_box, item1))

            if value == True:
                combo_box.setCurrentIndex(0)
            else:
                combo_box.setCurrentIndex(1)

            # Dodaj przycisk usuwający do trzeciej kolumny
            remove_button = QPushButton("", self)
            remove_button.setIcon(QIcon("./icons/bin.png"))
            remove_button.clicked.connect(lambda _, row=row_position: self.remove_row(row))
            self.table_widget.setCellWidget(row_position, 2, remove_button)




    def refresh_values(self):
        self.table_widget.setRowCount(0)

        newVarDict = {}
        for key, value in self.graphWidget.placesDict.items():
            newVarDict.update(value.variables)

        print(newVarDict, self.varDict, "dicts")
        for key, value in self.varDict.items():
            if key in newVarDict.keys():
                newVarDict.update({key: value})


        self.varDict = newVarDict
        self.graphWidget.variableDict = self.varDict
        self.populate_table()

