
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
from pydub import AudioSegment
from pydub.playback import play
import numpy as np
import threading
import time



class AudioStream(object):
    def __init__(self, file_path):
        self.app = pg.mkQApp()

        self.traces = dict()

        self.phase = 0
        self.t = np.arange(0, 3.0, 0.01)

        self.plot_widget = pg.PlotWidget()

        self.plot_widget.resize(1000, 600)

        self.plot_widget.show()

        self.audio_segment = AudioSegment.from_mp3(file_path)
        self.sample_rate = self.audio_segment.frame_rate
        self.num_channels = self.audio_segment.channels
        self.sample_width = self.audio_segment.sample_width
        self.audio_data = np.array(self.audio_segment.get_array_of_samples())

        self.CHUNK = 1024
        self.x = np.arange(0, 2 * self.CHUNK, 2)
        self.f = np.linspace(0, self.sample_rate / 2, self.CHUNK // 2)

        self.audio_position = 0

    def play_audio(self):
        play(self.audio_segment)

    def start(self):
        self.app.exec()
    
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

            if self.num_channels > 1:
                wf_data = wf_data.reshape((-1, self.num_channels)).mean(axis=1)

            wf_data = (wf_data / (2 ** (8 * self.sample_width - 1))) * 255.0 + 128
            self.draw("HAL", dataset_x=self.x, dataset_y=wf_data)

    def animate(self):
        timer = QtCore.QTimer()
        timer.timeout.connect(self.update)
        #timer.start(50)
        timer.start(int(1000 * self.CHUNK / self.sample_rate))  
        self.start()



# audio_stream = AudioStream("../output.mp3")

# audio_thread = threading.Thread(target=audio_stream.play_audio)

# audio_thread.start()

# time.sleep(0.1)

# audio_stream.animate()