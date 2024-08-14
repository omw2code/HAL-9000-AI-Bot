from pyqtgraph.Qt import QtCore, QtGui
from PyQt5.QtWidgets import QTextEdit
import datetime
from functools import partial
from collections import deque

class LoggerWidget(QTextEdit):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.logDialog = True
        self.logMetrics = False

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
        self._deactivation_message = deque(open('GUI/deactivation_protocol.txt').readlines())

    def init_ui(self):
        self.setReadOnly(True)
        self.setFixedSize(QtCore.QSize(600, 60))


    def output_hal_response(self):
        print(f"output_user_input:::::  Dialog log is {self.logDialog}")
        print(f"output_user_input::::: Metrics log is {self.logMetrics}")
        if(self.logDialog):
            with open('GUI/hal_output.txt', 'r') as file:
                text = 'HAL: '
                text += file.read()
                text += '\n'
                self.setTextColor(QtGui.QColor(255, 0, 0))
                self.insert_phrase_char(list(text))
                self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())


    def output_user_input(self):
        if(self.logDialog):
            with open('speech_output.txt', 'r') as file:
                line = file.readlines()
                text = line[0].removeprefix('New User Input to answer: ')
                text = ''.join(['User: ', text])
    
            with open("speech_output.txt", "w") as file:
                file.truncate(0)
            self.setTextColor(QtGui.QColor(255, 255, 255))
            self.insert_phrase_char(list(text))
            self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())

    def deactivation_log(self):
        self.log_timer = QtCore.QTimer()
        self.log_timer.timeout.connect(self.begin_deactivation)
        self.insert_phrase_char(list(self._deactivation_message.popleft()))
        self.log_timer.start(5000)


    def begin_deactivation(self):
        if len(self._deactivation_message) > 0:
            # print('in deactivate\n ')

            # self.setTextColor(QtGui.QColor('#8B0000'))
            self.setTextColor(QtGui.QColor('red'))
            self.insert_phrase_char(list(self._deactivation_message.popleft()))
            self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())
            # pass
        else:
            self.log_timer.stop()

    def start_logging(self):
        if(self.logMetrics):
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
    
    def setLogStatus(self):
        if(self.logDialog):
            self.logDialog = False
            self.logMetrics = True
        else:
            self.logDialog = True
            self.logMetrics = False
            self.log_timer.stop()