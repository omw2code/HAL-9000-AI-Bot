from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from pyqtgraph.Qt import QtCore
from PyQt5.QtCore import Qt

import GUI.loggerwidget as lw
import GUI.buttons as but
import GUI.graphwidget as gw

class GUI(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        #plot and logger
        self.plot_widget = gw.Graph()
        self.logger = lw.LoggerWidget()

        #Button config
        self.halButton = but.ButtonWidget('Disable HAL')
        self.dialogButton = but.ButtonWidget('Show Dialog')
        self.loggerButton = but.ButtonWidget('Show Logger')
        self.deactivateButton = but.ButtonWidget('DEACTIVATE HAL')

        #Button colors
        self.deactivateButton.setStyleSheet('background-color: #8B0000')
        self.halButton.setStyleSheet('Background-color: Red')

        #set up buttons enabled states
        self.dialogButton.setEnabled(False)
        self.deactivateButton.setEnabled(False)

        #if the dialog button is clicked, enable the loggerButton
        self.dialogButton.clicked.connect(self.dialogButton.disable_button)
        self.dialogButton.clicked.connect(self.loggerButton.enable_button)
        self.dialogButton.clicked.connect(self.logger.clear)
        self.dialogButton.clicked.connect(self.logger.setLogStatus)

        #if the logger button is clicked, enable the dialog button
        self.loggerButton.clicked.connect(self.loggerButton.disable_button)
        self.loggerButton.clicked.connect(self.dialogButton.enable_button)
        self.loggerButton.clicked.connect(self.logger.clear)
        self.loggerButton.clicked.connect(self.logger.setLogStatus)
        self.loggerButton.clicked.connect(self.logger.start_logging)

        #if the hal button is clicked
        self.halButton.clicked.connect(self.halButton.halClicked)
        self.halButton.clicked.connect(self.deactivateButton.enable_button)

        #if DEACTIVATE HAL is clicked
        self.deactivateButton.clicked.connect(self.loggerButton.disable_button)
        self.deactivateButton.clicked.connect(self.dialogButton.disable_button)
        self.deactivateButton.clicked.connect(self.halButton.disable_button)
        self.deactivateButton.clicked.connect(self.deactivateButton.disable_button)
        self.deactivateButton.clicked.connect(self.logger.clear)
        self.deactivateButton.clicked.connect(self.plot_widget.run_deactivate)
        self.deactivateButton.clicked.connect(self.logger.deactivation_log)

        
        #GUI layout set up
        self.vlayout = QVBoxLayout()
        self.vlayout.addWidget(self.plot_widget)
        self.vlayout.addWidget(self.logger)

        self.vlayout2 = QVBoxLayout()
        self.vlayout2.addWidget(self.halButton)
        self.vlayout2.addWidget(self.dialogButton)
        self.vlayout2.addWidget(self.loggerButton)
        self.vlayout2.addWidget(self.deactivateButton)

        self.hlayout = QHBoxLayout()
        self.hlayout.addLayout(self.vlayout)
        self.hlayout.addLayout(self.vlayout2)
        self.setLayout(self.hlayout)