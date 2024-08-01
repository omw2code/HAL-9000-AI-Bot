import GUI.audio_visualizer as av
import workerthread as wt

from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QApplication
import sys

def main() -> None:
    app = QApplication([])
    gui = av.GUI()
    worker = wt.WorkerThread()
    thread = QThread()
    worker.moveToThread(thread)

    worker.visual_available.connect(gui.plot_widget.animate)
    worker.log_hal_output.connect(gui.logger.output_hal_response)
    worker.log_user_input.connect(gui.logger.output_user_input)
    
    thread.started.connect(worker.run)
    thread.start()
    gui.dialogButton.clicked.connect(worker.start_logging_convo)
    gui.show()
    sys.exit(app.exec_())
    


if __name__ == "__main__":
    main()
