# from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
# from PyQt5.QtCore import QTimer
#
# from main import GraphWidget
#
#
# class MainWindow(QWidget):
#     def __init__(self):
#         super().__init__()
#
#         self.label = QLabel("Czas: 0", self)
#
#         layout = QVBoxLayout(self)
#         layout.addWidget(self.label)
#
#         self.timer = QTimer(self)
#         self.timer.timeout.connect(self.update_timer)
#         self.timer.start(500)  # Timer będzie wywoływany co 1000 milisekund (1 sekunda)
#
#     def update_timer(self):
#         # Ta metoda będzie wywoływana za każdym razem, gdy timer osiągnie timeout
#         current_time = int(self.label.text().split(":")[1])
#         current_time += 1
#         self.label.setText(f"Czas: {current_time}")
#
# if __name__ == '__main__':
#     import sys
#
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec_())