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
        font = QtGui.QFont('Courier New', 10)
        self.setFont(font)
        self.setFixedSize(QtCore.QSize(100, 80))
        self.setRed = False

    def halClicked(self):
        if(self.setRed):
            self.setStyleSheet("Background-color: red")
            self.setText("Disable H.A.L")
            self.setRed = False
        else:
            self.setStyleSheet("Background-color: green")
            self.setText("Enable H.A.L")
            self.setRed = True
    
    def enable_button(self):
        self.setEnabled(True)
        
    def disable_button(self):
        self.setEnabled(False)
    
    def deactivate_clicked(self):
        self.deactivate.emit("Deactivate HAL")

