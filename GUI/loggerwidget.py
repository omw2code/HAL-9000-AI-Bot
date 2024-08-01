from pyqtgraph.Qt import QtCore, QtGui
from PyQt5.QtWidgets import QTextEdit
import datetime
from functools import partial
class LoggerWidget(QTextEdit):
    def __init__(self):
        super().__init__()
        self.init_ui()

        #log messages
        self.color_counter = 0
        self.colors = [
            #Green color rgb
            QtGui.QColor(0, 255, 0),
            #Yellow
            QtGui.QColor(255, 255, 0),
            #White
            QtGui.QColor(255, 255, 255)
        ]
        self.textList = [
            f"{datetime.datetime.now()} | Status: GOOD | System Uptime: 4 hours - System stable\n",
            f"{datetime.datetime.now()} | Status: OK | CPU Usage: 45%, Memory Usage: 30% - System running normally.\n",
            f"{datetime.datetime.now()} | Status: INFO | Disk Space: 100 GB free. Battery: 80% - System ready.\n"
        ]

    def init_ui(self):
        self.isReadOnly = True
        self.setFixedSize(QtCore.QSize(800, 80))
    
    def output_hal_response(self):
        with open('GUI/hal_output.txt', 'r') as file:
            line = file.readlines()
            text = line[0]
            self.setTextColor(QtGui.QColor(255, 0, 0))
            self.insert_phrase_char(list(text))
            self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())
        
    def output_user_input(self):
        with open('speech_output.txt', 'r') as file:
            line = file.readlines()
            text = line[0]
            
            self.insert_phrase_char(list(text))
            self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())
            

    def start_logging(self):
        #log 3 different things: current OS status, current temperature status, current 
        self.log_timer = QtCore.QTimer()
        self.log_timer.timeout.connect(self.log_message)
        self.log_timer.start(3000)
        
    
    def log_message(self) -> None:
        self.color_counter = (self.color_counter + 1) % len(self.colors)
        color = self.colors[self.color_counter]
        self.setTextColor(color)
        
        text = list(self.textList[self.color_counter])
        self.insert_phrase_char(text)
        self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())

    def insert_phrase_char(self, text):
        if len(text) > 0:
            cursor = self.textCursor()

            next_char = text.pop(0)
            cursor.insertText(next_char)
            QtCore.QTimer.singleShot(10, partial(self.insert_phrase_char, text))