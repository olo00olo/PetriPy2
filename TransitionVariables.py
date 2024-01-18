from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QComboBox, QTableWidget, QTableWidgetItem, QMessageBox

from Saver import saver


class TransitionVariables(QDialog):
    def __init__(self, transition, graphWidget, mainWindow):
        super().__init__()

        self.transition = transition
        self.graphWidget = graphWidget

        self.setWindowTitle("Table Dialog")

        self.table_widget = QTableWidget(self)
        self.table_widget.setColumnCount(3)
        self.table_widget.setHorizontalHeaderLabels(["Column 1", "Column 2", "Remove"])

        self.table_widget.horizontalHeader().setVisible(False)
        # self.table_widget.verticalHeader().setVisible(False)

        add_row_button = QPushButton("Add Row", self)
        add_row_button.clicked.connect(self.add_row)

        apply_button = QPushButton("Apply", self)
        apply_button.clicked.connect(self.apply)

        layout = QVBoxLayout(self)
        layout.addWidget(self.table_widget)
        layout.addWidget(add_row_button)
        layout.addWidget(apply_button)


        self.empty_column_counter = 0

        self.mainWindow = mainWindow
        self.init_combo_box_options()
        self.initial_table()




    def initial_table(self):
        expression = self.transition.variables
        if expression != "":
            expression = expression.split()

            for x in range(len(expression)):
                self.add_row()
                if x % 2 == 0:
                    if expression[x][0] == "~":
                        self.table_widget.cellWidget(x, 0).setCurrentIndex(1)

                        index = self.combo_box2_options.index(expression[x][1:])
                        self.table_widget.cellWidget(x, 1).setCurrentIndex(index)

                    else:
                        index = self.combo_box2_options.index(expression[x])
                        self.table_widget.cellWidget(x, 1).setCurrentIndex(index)

                else:
                    if expression[x] == "OR":
                        self.table_widget.cellWidget(x, 1).setCurrentIndex(1)
                    if expression[x] == "AND":
                        self.table_widget.cellWidget(x, 1).setCurrentIndex(2)




    def init_combo_box_options(self):
        varList = []
        # for key, value in self.graphWidget.placesDict.items():
        #     varList.extend(list(value.variables.keys()))
        for key, value in self.graphWidget.variableDict.items():
            varList.append(key)


        combo_box1_options = ["", "~"]
        self.combo_box1_options = combo_box1_options

        combo_box2_options = [""]
        combo_box2_options.extend(varList)
        combo_box2_options = list(set(combo_box2_options))
        self.combo_box2_options = combo_box2_options

        combo_box3_options = ["", "OR", "AND"]
        self.combo_box3_options = combo_box3_options

    def add_row(self):
        row_position = self.table_widget.rowCount()

        self.table_widget.insertRow(row_position)

        if row_position % 2 == 0:
            combo_box1 = QComboBox(self)
            combo_box1.addItems(self.combo_box1_options)
            combo_box1.setCurrentIndex(0)
            self.table_widget.setCellWidget(row_position, 0, combo_box1)

            combo_box2 = QComboBox(self)
            combo_box2.addItems(self.combo_box2_options)
            combo_box2.setCurrentIndex(0)
            self.table_widget.setCellWidget(row_position, 1, combo_box2)
        else:
            empty_item = QTableWidgetItem()
            empty_item.setFlags(empty_item.flags() & ~Qt.ItemIsEnabled)
            self.table_widget.setItem(row_position, 0, empty_item)

            combo_box3 = QComboBox(self)
            combo_box3.addItems(self.combo_box3_options)
            combo_box3.setCurrentIndex(0)
            self.table_widget.setCellWidget(row_position, 1, combo_box3)

        # combo_box2 = QComboBox(self)
        # combo_box2.addItems(self.combo_box2_options)
        # self.table_widget.setCellWidget(row_position, 1, combo_box2)

        remove_button = QPushButton("Remove", self)
        remove_button.clicked.connect(lambda _, row=row_position: self.remove_row(row))
        self.table_widget.setCellWidget(row_position, 2, remove_button)

    def remove_row(self, row):
        widget = self.table_widget.cellWidget(row, 0)
        if isinstance(widget, QComboBox):
            if row + 1 >= 0:
                self.table_widget.removeRow(row + 1)
                self.indexRemap()
                self.table_widget.removeRow(row)
                self.indexRemap()
        else:
            if row - 1 >= 0:
                self.table_widget.removeRow(row)
                self.indexRemap()
                self.table_widget.removeRow(row - 1)
                self.indexRemap()

    def indexRemap(self):
        for r in range(self.table_widget.rowCount()):
            remove_button = self.table_widget.cellWidget(r, 2)
            if remove_button:
                remove_button.clicked.disconnect()
                remove_button.clicked.connect(lambda state, row=r: self.remove_row(row))

    def apply(self):
        print(self.table_widget.rowCount())
        if self.table_widget.rowCount() < 1:
            self.transition.setVariables("")
            print("XD")

        else:
            expression = ""

            rows = self.table_widget.rowCount()

            if rows % 2 == 0 and rows > 0:
                newRange = rows - 1
            else:
                newRange = rows

            for x in range(newRange):
                if x % 2 == 0:
                    if self.table_widget.cellWidget(x, 1).currentText() == "":
                        msgBox = QMessageBox()
                        msgBox.information(self, "Information", "Variable cell can't be empty. Delete or choose variable.")
                    else:
                        if self.table_widget.cellWidget(x, 0).currentText() == "~":
                            expression += "~" + self.table_widget.cellWidget(x, 1).currentText() + " "
                        else:
                            expression += self.table_widget.cellWidget(x, 1).currentText() + " "

                else:
                    if self.table_widget.cellWidget(x, 1).currentText() == "":
                        msgBox = QMessageBox()
                        msgBox.information(self, "Information", "Operator cell can't be empty. Delete or choose operator.")
                    elif self.table_widget.cellWidget(x, 1).currentText() == "OR":
                        expression += "OR "
                    elif self.table_widget.cellWidget(x, 1).currentText() == "AND":
                        expression += "AND "

            if rows > 0:
                expression = expression[:-1]
                self.transition.setVariables(expression)
                self.graphWidget.undoHeap.append(saver(self.graphWidget, "heap"))
                self.graphWidget.redoHeap = []
