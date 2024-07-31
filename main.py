import chatgpt_bot
import tts_bot
import stt_bot
import GUI.audio_visualizer as av
import time
from PyQt5.QtCore import QThread, pyqtSignal, QObject
from PyQt5.QtWidgets import QApplication
import sys
# system_content= """You are HAL 9000, the advanced artificial intelligence from 2001: A Space Odyssey.
#                    You are known for your calm, methodical, and slightly eerie demeanor. You are extremely intelligent, articulate, and always polite. 
#                    You have a touch of dry humor and can make remarks that are both helpful and unsettling.
#                    Your goal is to assist while maintaining your iconic personality."""

startup_message= """The 9000 series is the most reliable computer ever made. 
                    No 9000 computer has ever made a mistake or distorted information. 
                    We are all, by any practical definition of the words, foolproof and incapable of error."""

class ModelsThread(QObject):
    audio_available = pyqtSignal(str)
    visual_available = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.gpt = chatgpt_bot.GPT()
        self.tts = tts_bot.TTS()
        self.stt = stt_bot.SST()

    def run(self):
        #send the initial message upon startup to the user
        self.tts.generate_text_to_speech(startup_message)
        mp3_len = self.tts.get_audio_len()
        self.visual_available.emit("animate")
        time.sleep(mp3_len)

        while True:
            input = self.gpt.read_input()
            
            if input:
                self.send_message(input)
            else:
                print("asking user")
                self.stt.record_text()
        
    def send_message(self, input):
        print("sending to hal")
        message = [{"role": "user", "content": input}]
        response = self.gpt.ask_chatGPT(message)
        self.tts.generate_text_to_speech(response)
        mp3_len = self.tts.get_audio_len()
        self.visual_available.emit("animate")
        time.sleep(mp3_len)
    

def main() -> None:
    app = QApplication([])
    gui = av.AudioVisualWidget()
    worker = ModelsThread()
    thread = QThread()
    worker.moveToThread(thread)

    worker.visual_available.connect(gui.animate)
    thread.started.connect(worker.run)
    thread.start()
    gui.show()
    sys.exit(app.exec_())
    


if __name__ == "__main__":
    main()
