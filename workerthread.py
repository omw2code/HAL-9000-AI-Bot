import chatgpt_bot
import tts_bot
import stt_bot
import time
from PyQt5.QtCore import pyqtSignal, QObject

startup_message= "The 9000 series is the most reliable computer ever made. No 9000 computer has ever made a mistake or distorted information. We are all, by any practical definition of the words, foolproof and incapable of error.\n"

class WorkerThread(QObject):
    log_hal_output = pyqtSignal(str)
    log_user_input = pyqtSignal(str)
    visual_available = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.gpt = chatgpt_bot.GPT()
        self.tts = tts_bot.TTS()
        self.stt = stt_bot.SST()
        self.log_conversation = True

    def run(self):
        #send the initial message upon startup to the user
        self.tts.generate_text_to_speech(startup_message)
        mp3_len = self.tts.get_audio_len()
        self.output_hal_response(startup_message)

        if(self.log_conversation):
            self.log_hal_output.emit("log output")
    
        self.visual_available.emit("animate")
        time.sleep(mp3_len)

        while True:
            input = self.gpt.read_input()
            
            if input:
                if(self.log_conversation):
                    self.log_user_input.emit("log input")
                self.send_message(input)
            else:
                print("asking user")
                self.stt.record_text()
        
    def send_message(self, input):
        print("sending to hal")
        message = [{"role": "user", "content": input}]
        response = self.gpt.ask_chatGPT(message)
        self.output_hal_response(response)
        self.tts.generate_text_to_speech(response)
        mp3_len = self.tts.get_audio_len()
        if(self.log_conversation):
            self.log_hal_output.emit('log output')
        self.visual_available.emit("animate")
        time.sleep(mp3_len)
    
    def start_logging_convo(self):
        if(self.log_conversation):
            self.log_conversation = False
        else:
            self.log_conversation = True

    def output_hal_response(self, response):
        try:
            with open("GUI/hal_output.txt", "w") as file:
                file.truncate(0)
                file.write(response)
        except Exception as e:
            print("An error has occurred: {0}".format(e))
        return