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
        self.time = 1000
        self.timer.timeout.connect(lambda: self.update_timer())

        self.item = item



    @pyqtSlot()
    def update_timer(self):
        # current_time = int(self.label.text().split(":")[1])
        # current_time += 1
        self.trigger.emit()


    def start_simulation(self):
        self.timer.start(self.time)

    def stop_simulation(self):
        self.timer.stop()

    def change_speed(self, decrement=100):
        self.time = max(100, self.time - decrement)
        if self.timer.isActive():
            self.timer.start(self.time)


