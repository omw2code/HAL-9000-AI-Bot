import pyqtgraph
from pyqtgraph.Qt import QtCore
from PyQt5.QtCore import QThread, QObject, pyqtSignal
from pydub import AudioSegment
from pydub.playback import play
import numpy as np
import time

class Graph(pyqtgraph.PlotWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.resize(800, 480)
        self.timer = QtCore.QTimer()
        self.tet = QThread()

    def config(self):
        self.clear()
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
            self.traces[name] = self.plot(pen='r')
            self.setYRange(0, 255, padding=0)
            self.setXRange(0, 2 * self.CHUNK, padding=0.005)

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


class AudioThread(QObject):
    finished = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()
    
    def play_audio(self):
        self.audio_segment = AudioSegment.from_mp3("GUI/output.mp3")
        play(self.audio_segment)
        self.finished.emit()