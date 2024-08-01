from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout

import GUI.loggerwidget as lw
import GUI.buttons as but
import GUI.graphwidget as gw

class GUI(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.plot_widget = gw.Graph()
        self.logger = lw.LoggerWidget()
        
        self.vlayout = QVBoxLayout()

        self.vlayout.addWidget(self.plot_widget)
        self.vlayout.addWidget(self.logger)

        self.halButton = but.ButtonWidget('Disable H.A.L')
        self.dialogButton = but.ButtonWidget('Show Dialog')
        self.loggerButton = but.ButtonWidget('Show Logger')

        #Button clicked set up
        self.dialogButton.clicked.connect(self.logger.clear)
        self.loggerButton.clicked.connect(self.logger.start_logging)
        self.halButton.clicked.connect(self.halButton.halClicked)


        #GUI layout set up
        self.vlayout2 = QVBoxLayout()
        self.vlayout2.addWidget(self.halButton)
        self.vlayout2.addWidget(self.dialogButton)
        self.vlayout2.addWidget(self.loggerButton)

        self.hlayout = QHBoxLayout()
        self.hlayout.addLayout(self.vlayout)
        self.hlayout.addLayout(self.vlayout2)
        self.setLayout(self.hlayout)