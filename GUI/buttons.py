from pyqtgraph.Qt import QtCore, QtGui
from PyQt5.QtWidgets import QPushButton

class ButtonWidget(QPushButton):
    enableHal = QtCore.pyqtSignal(str)
    deactivate = QtCore.pyqtSignal(str)
    def __init__(self, name):
        super().__init__()
        self.init_ui()
        self.setText(name)

    def init_ui(self):
        self.font = QtGui.QFont('Courier New', 9)
        self.setFont(self.font)
        self.setFixedSize(QtCore.QSize(100, 80))
        self.setRed = False

    def halClicked(self):
        if(self.setRed):
            self.setStyleSheet("Background-color: red; color: white")
            self.setText("Disable H.A.L")
            self.setRed = False
        else:
            self.setStyleSheet("Background-color: green; color: white")
            self.setText("Enable H.A.L")
            self.setRed = True
    
    def enable_button(self):
        self.setEnabled(True)
        self.setStyleSheet("color: white")
        self.font.setBold(True)
        self.setFont(self.font)
        
    def disable_button(self):
        self.setEnabled(False)
        self.setStyleSheet("color: grey")
        self.font.setBold(False)
        self.setFont(self.font)
    
    def deactivate_clicked(self):
        self.deactivate.emit("Deactivate HAL")

    def start_flashing(self):
        self.timer = QtCore.QTimer()

        self.timer.timeout.connect(self.flash_red)
        self.timer.start(1200)
    
    def flash_red(self):
        if(self.setRed):
            self.setStyleSheet("Background-color: #8B0000; color: grey")
            self.font.setBold(False)
            self.setFont(self.font)
            self.setRed = False
        else:
            self.setStyleSheet("Background-color: red; color: white")
            self.font.setBold(True)
            self.setFont(self.font)
            self.setRed = True

    def change_deactivate_state(self):
        if(self.setRed):
            self.setEnabled(False)
            self.setStyleSheet("Background-color: #8B0000; color: grey")
            self.setRed = False
        else:
            self.setEnabled(True)
            self.setStyleSheet("Background-color: red; color: white")
            self.setRed = True
