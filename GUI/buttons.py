from pyqtgraph.Qt import QtCore, QtGui
from PyQt5.QtWidgets import QPushButton

class ButtonWidget(QPushButton):
    def __init__(self, name):
        super().__init__()
        self.init_ui()
        self.setText(name)

    def init_ui(self):
        font = QtGui.QFont('Courier New', 20)
        self.setFont(font)
        self.setFixedSize(QtCore.QSize(200, 150))
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
