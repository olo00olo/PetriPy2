# from PyQt5.QtCore import Qt
# from PyQt5.QtWidgets import QDialog, QTableWidget, QVBoxLayout, QTableWidgetItem, QCheckBox, QPushButton
#
#
# class InitialVariables(QDialog):
#     def __init__(self, graphWidget):
#         super().__init__()
#
#         self.graphWidget = graphWidget
#
#         self.table_widget = QTableWidget(self)
#         self.table_widget.setColumnCount(2)
#         self.table_widget.setHorizontalHeaderLabels(["Key", "Checkbox"])
#
#         layout = QVBoxLayout(self)
#
#         apply_button = QPushButton("Apply", self)
#         apply_button.clicked.connect(self.apply)
#
#
#
#         layout.addWidget(self.table_widget)
#         layout.addWidget(apply_button)
#
#         self.varDict = {}
#
#     def updateVariables(self):
#         self.varDict = {}
#         newVarDict = {}
#         for key, value in self.graphWidget.placesDict.items():
#             for key2, value2 in value.variables.items():
#                 # self.varDict.update({key2: False})
#                 newVarDict.update({key2: False})
#
#         for key, value in self.varDict.items():
#             if key in newVarDict.keys():
#                 newVarDict.update(key)
#
#         self.varDict = newVarDict
#         print(self.varDict, 'dict')
#
#         self.populate_table()
#
#     def populate_table(self):
#         row_position = 0
#         self.table_widget.setRowCount(len(self.varDict))
#
#
#         for key, value in self.varDict.items():
#             key_item = QTableWidgetItem(str(key))
#             key_item.setFlags(key_item.flags() & ~Qt.ItemIsEnabled)
#             print(key_item, "key")
#             self.table_widget.setItem(row_position, 0, key_item)
#
#             checkbox = QCheckBox()
#             checkbox.setChecked(value)
#             self.table_widget.setCellWidget(row_position, 1, checkbox)
#
#             row_position += 1
#
#
#     def apply(self):
#         print(self.table_widget.rowCount(), "count")
#         for row in range(self.table_widget.rowCount()):
#             v = self.table_widget.item(row, 0).text()
#             s = self.table_widget.cellWidget(row, 1).checkState()
#
#             if s == 2:
#                 s = 1
#             else:
#                 s = 0
#
#             self.varDict.update({v: s})
#         self.graphWidget.variableDict = self.varDict
#
