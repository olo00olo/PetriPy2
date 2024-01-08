from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import QTimer, pyqtSlot, pyqtSignal

from Matrix import Matrix


class Simulator(QWidget):
    trigger = pyqtSignal()

    def __init__(self, item):
        print(self)
        super().__init__()

        self.label = QLabel("Czas: 0", self)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label)

        self.timer = QTimer(self)
        self.timer.timeout.connect(lambda: self.update_timer(item))
        self.time = 1000



    # @pyqtSlot()
    def update_timer(self, item):
        # Ta metoda będzie wywoływana za każdym razem, gdy timer osiągnie timeout
        current_time = int(self.label.text().split(":")[1])
        current_time += 1
        print(current_time)
        self.label.setText(f"Czas: {current_time}")
        self.trigger.emit()
        print("XDDDDDDDDDDDD")


    def start_simulation(self):
        # self.cMatrix = Matrix.getCMatrix()
        # print(self.cMatrix)
        # self.timer.start(500)  # 0.5 sekundy
        self.timer.start(self.time)

    def stop_simulation(self):
        self.timer.stop()


