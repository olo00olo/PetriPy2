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

        self.uVar = {}
        self.varDict = {}

        self.init_ui()

    def init_ui(self):
        dock_widget_content = QWidget(self)
        dock_widget_layout = QVBoxLayout(dock_widget_content)

        self.table_widget = QTableWidget(self)
        self.table_widget.setColumnCount(3)
        # self.table_widget.setHorizontalHeaderLabels(["Column 1", "Column 2", "Column 3"])
        self.table_widget.horizontalHeader().setVisible(False)

        self.table_widget.setColumnWidth(1, 55)  # Szerokość drugiej kolumny
        self.table_widget.setColumnWidth(2, 50)


        button = QPushButton("Add variable", self)
        button.clicked.connect(self.add_row)

        dock_widget_layout.addWidget(self.table_widget)
        dock_widget_layout.addWidget(button)

        self.setWidget(dock_widget_content)

    def add_row(self):
        row_position = self.table_widget.rowCount()

        if row_position > 0:
            if self.table_widget.cellWidget(row_position - 1, 0).text() == "":
                msgBox = QMessageBox()
                msgBox.information(self, "Information", "Change null variable first")
                return


        self.table_widget.insertRow(row_position)

        item1 = QTableWidgetItem("")
        self.table_widget.setItem(row_position, 0, item1)
        line_edit = QLineEdit(self)
        line_edit.setText("")
        self.table_widget.setCellWidget(row_position, 0, line_edit)
        line_edit.editingFinished.connect(lambda: self.new_var(line_edit, item1))


        combo_box = QComboBox(self)
        combo_box.addItems(["False", "True"])
        combo_box.setCurrentIndex(0)
        self.table_widget.setCellWidget(row_position, 1, combo_box)
        combo_box.currentIndexChanged.connect(lambda index: self.new_var(combo_box, item1))


        self.uVar.update({line_edit: [combo_box, ""]})


        remove_button = QPushButton("", self)
        remove_button.setIcon(QIcon("./icons/bin.png"))
        remove_button.clicked.connect(lambda _, row=row_position: self.remove_row(row))
        self.table_widget.setCellWidget(row_position, 2, remove_button)

    def new_var(self, widget, item):
        if isinstance(widget, QComboBox):
            k = self.table_widget.cellWidget(item.row(), 0).text()
            if k == '':
                msgBox = QMessageBox()
                msgBox.information(self, "Information", "Change null variable first")

            else:
                if widget.currentText() == "True":
                    self.graphWidget.variableDict.update({k: True})
                else:
                    self.graphWidget.variableDict.update({k: False})

        else:
            a = self.table_widget.cellWidget(item.row(), 0)
            b = self.table_widget.cellWidget(item.row(), 1).currentText()

            if a.text() == '':
                msgBox = QMessageBox()
                msgBox.information(self, "Information", "Change null variable first")
                return

            for key, value in self.graphWidget.placesDict.items():
                if a.text() in value.variables:
                    msgBox = QMessageBox()
                    msgBox.information(self, "Information", "Variable already exists")
                    return

            for key, value in self.graphWidget.transitionsDict.items():
                sp = value.variables.split()
                for x in range(len(sp)):
                    if x % 2 == 0:
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

            if b == "True":
                self.graphWidget.variableDict.update({a.text(): True})
            else:
                self.graphWidget.variableDict.update({a.text(): False})

            if self.uVar[widget][1] in self.graphWidget.variableDict.keys():
                del self.graphWidget.variableDict[self.uVar[widget][1]]


            self.uVar[a] = [self.uVar[a][0], a.text()]

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
                            msgBox.information(self, "Information", "Variable connected to transition T" + str(key))
                            return
                    elif sp[x] == temp:
                        msgBox = QMessageBox()
                        msgBox.information(self, "Information", "Variable connected to transition T" + str(key))
                        return

        self.table_widget.removeRow(row)

        if temp in self.graphWidget.variableDict.keys():
            self.graphWidget.variableDict.pop(temp)

        for r in range(self.table_widget.rowCount() - 1, -1, -1):
            remove_button = self.table_widget.cellWidget(r, 2)
            if remove_button:
                remove_button.clicked.disconnect()
                remove_button.clicked.connect(lambda _, row=r: self.remove_row(row))


    def refresh_table(self):
        for row in range(self.table_widget.rowCount()):
            print("XDD")
            a = self.table_widget.cellWidget(row, 0).text()
            print(row, self.table_widget.cellWidget(row, 0).text(), self.graphWidget.variableDict[a])
            self.table_widget.cellWidget(row, 1).setCurrentText(str(self.graphWidget.variableDict[a]))
