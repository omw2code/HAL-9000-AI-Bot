from pyqtgraph.Qt import QtCore, QtGui
from PyQt5.QtWidgets import QWidget, QTextEdit, QVBoxLayout, QHBoxLayout,QPushButton
from PyQt5.QtCore import QThread, QObject, pyqtSignal, QSize
import pyqtgraph as pg
from pydub import AudioSegment
from pydub.playback import play
import numpy as np
import time, datetime
import os

class AudioThread(QObject):
    finished = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()
    
    def play_audio(self):
        self.audio_segment = AudioSegment.from_mp3("GUI/output.mp3")
        play(self.audio_segment)
        self.finished.emit()

#TODO: CLEAN UP CODE AND MOVE WIDGETS TO INDIVIDUAL FILES //////////////////////
class GUI(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.start_dialog()

    def init_ui(self):
        self.app = pg.mkQApp()
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.resize(800, 480)

        self.logger = QTextEdit()
        self.logger.isReadOnly = True
        self.logger.setFixedSize(QSize(800, 80))
        
        self.vlayout = QVBoxLayout()

        self.vlayout.addWidget(self.plot_widget)
        self.vlayout.addWidget(self.logger)
        # self.setLayout(self.vlayout)

        #Button style config
        self.halButton = QPushButton('Disable H.A.L.')
        self.dialogButton = QPushButton('Show Dialog')
        self.loggerButton = QPushButton('Show Logger')
        font = QtGui.QFont('Courier New', 20)
        self.halButton.setFont(font)
        self.dialogButton.setFont(font)
        self.loggerButton.setFont(font)
        self.loggerButton.setDisabled(True)
        self.halButton.setFixedSize(QSize(200, 150))
        self.dialogButton.setFixedSize(QSize(200, 150))
        self.loggerButton.setFixedSize(QSize(200, 150))

        #Button clicked set up
        self.dialogButton.clicked.connect(self.start_dialog)
        self.loggerButton.clicked.connect(self.start_logging)

        #GUI layout set up
        self.vlayout2 = QVBoxLayout()
        self.vlayout2.addWidget(self.halButton)
        self.vlayout2.addWidget(self.dialogButton)
        self.vlayout2.addWidget(self.loggerButton)

        self.hlayout = QHBoxLayout()
        self.hlayout.addLayout(self.vlayout)
        self.hlayout.addLayout(self.vlayout2)
        self.setLayout(self.hlayout)

        # self.plot_widget.show()
        self.timer = QtCore.QTimer()
        self.tet = QThread()
    
    def start_dialog(self):
        self.dialogButton.setDisabled(True)
        self.loggerButton.setDisabled(False)

        #if the signal was emitted from the logger button, stop this
        #if there is text, display it

        with open('speech_output.txt', 'r') as file:
            text = file.readlines()
            

    
    def start_logging(self):
        self.loggerButton.setDisabled(True)
        self.dialogButton.setDisabled(False)
        
        #log 3 different things: current OS status, current temperature status, current 
        self.log_timer = QtCore.QTimer()
        self.log_timer.timeout.connect(self.log_message)
        self.log_timer.start(2000)
        
    
    def log_message(self) -> None:
            # self.logger.moveCursor(self.logger.verticalScrollBar().maximum())
            # self.logger.setTextColor(QtGui.QColor(255, 51, 0))
            # self.logger.setPlainText(message)

            # # Scroll to the bottom to show the latest messages
            # self.logger.verticalScrollBar().setValue(self.logger.verticalScrollBar().maximum())
        self.text_phrase = list(f"{datetime.datetime.now()} | Status: OK | Log message tests.\n")
        self.insert_phrase_char()
        self.logger.verticalScrollBar().setValue(self.logger.verticalScrollBar().maximum())

    def insert_phrase_char(self):
        if len(self.text_phrase) > 0:
            cursor = self.logger.textCursor()
            next_char = self.text_phrase.pop(0)
            cursor.insertText(next_char)
            QtCore.QTimer.singleShot(10, self.insert_phrase_char)

    def config(self):
        self.plot_widget.clear()
        self.traces = dict()
        self.audio_position = 0
        self.CHUNK = 1024
        self.x = np.arange(0, 2 * self.CHUNK, 2)
        self.audio_segment = AudioSegment.from_mp3("GUI/output.mp3")
        self.sample_rate = self.audio_segment.frame_rate
        self.num_channels = self.audio_segment.channels
        self.sample_width = self.audio_segment.sample_width
        self.audio_data = np.array(self.audio_segment.get_array_of_samples())

    def draw(self, name, dataset_x, dataset_y):
        if name in self.traces:
            self.traces[name].setData(dataset_x, dataset_y)
        else:
            self.traces[name] = self.plot_widget.plot(pen='r')
            self.plot_widget.setYRange(0, 255, padding=0)
            self.plot_widget.setXRange(0, 2 * self.CHUNK, padding=0.005)

    def update(self):
        if self.audio_position + self.CHUNK * self.num_channels < len(self.audio_data):
            wf_data = self.audio_data[self.audio_position:self.audio_position + self.CHUNK * self.num_channels]
            self.audio_position += self.CHUNK * self.num_channels
            #num channels may not be the expected number im thinking
            if self.num_channels > 1:
                wf_data = wf_data.reshape((-1, self.num_channels)).mean(axis=1)

            wf_data = (wf_data / (2 ** (8 * self.sample_width - 1))) * 255.0 + 128
            self.draw("HAL", dataset_x=self.x, dataset_y=wf_data)
        else:
            if self.timer.isActive():
                print("Stopping timer")
                self.timer.stop()

    def animate(self):
        #TODO: look at the logic of this and maybe change it to improve the latency
        self.stop()
        self.config()
        #this timer aint working right
        self.timer = QtCore.QTimer()
        self.tet = QThread()

        worker = AudioThread()
        worker.moveToThread(self.tet)
        worker.finished.connect(self.tet.quit)
        self.tet.started.connect(worker.play_audio)
        self.tet.start()

        time.sleep(0.1)
        #TODO: Check timers timeout
        self.timer.timeout.connect(self.update)
        self.timer.start(int(1000 * self.CHUNK / self.sample_rate))

    def stop(self):
        if self.timer.isActive():
            self.timer.stop()
        if self.tet.isRunning():
            self.tet.quit()
            self.tet.wait()