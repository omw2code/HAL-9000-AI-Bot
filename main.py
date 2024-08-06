import GUI.audio_visualizer as av
import workerthread as wt

import chatgpt_bot
import tts_bot
import stt_bot

from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QApplication
import sys
import qdarkstyle

def main() -> None:
    gpt = chatgpt_bot.GPT()
    tts = tts_bot.TTS()
    stt = stt_bot.SST()

    app = QApplication([])
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    gui = av.GUI()
    worker = wt.WorkerThread(gpt,tts,stt)



    worker.visual_available.connect(gui.plot_widget.animate)
    worker.log_hal_output.connect(gui.logger.output_hal_response)
    worker.log_user_input.connect(gui.logger.output_user_input)
    gui.halButton.clicked.connect(worker.enable_or_disable_HAL)
    gui.deactivateButton.clicked.connect(worker.killworker)
    gui.dialogButton.clicked.connect(worker.start_logging_convo)

    thread = QThread()
    worker.moveToThread(thread)
    thread.started.connect(worker.run)
    thread.start()
    
    gui.show()
    
    sys.exit(app.exec_())
    


if __name__ == "__main__":
    main()
