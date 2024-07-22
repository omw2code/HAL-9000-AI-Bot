
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import pyaudio
import numpy as np
import sys
import struct



class AudioStream(object):
    def __init__(self, object):
        self.app = pg.mkQApp()

        self.traces = dict()

        self.phase = 0
        self.t = np.arange(0, 3.0, 0.01)

        self.plot_widget = pg.PlotWidget()

        self.plot_widget.resize(1000, 600)

        self.plot_widget.show()


        #pyaudio
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
        self.CHUNK = 1024 * 2

        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            output=True,
            frames_per_buffer=self.CHUNK
        )

        self.x = np.arange(0, 2 * self.CHUNK, 2)
        self.f = np.linspace(0, self.RATE / 2, self.CHUNK // 2)

    def start(self):
        self.app.exec()
    
    def draw(self, name, dataset_x, dataset_y):
        if name in self.traces:
            self.traces[name].setData(dataset_x, dataset_y)
        else:
            self.traces[name] = self.plot_widget.plot(pen='c')
            self.plot_widget.setYRange(0, 255, padding=0)
            self.plot_widget.setXRange(0, 2 * self.CHUNK, padding=0.005)
    
    def update(self):
        wf_data = self.stream.read(self.CHUNK)

        #wf_data = struct.unpack(str(self.CHUNK) + 'h', wf_data)
        wf_data = np.array(wf_data, dtype='h')
        wf_data = (wf_data / 32768.0) * 255.0 + 128
        self.draw("HAL", dataset_x=self.x, dataset_y=wf_data)

    def animate(self):
        timer = QtCore.QTimer()
        timer.timeout.connect(self.update)
        timer.start(20)
        self.start()



a = AudioStream("test.mp3")

a.animate()









