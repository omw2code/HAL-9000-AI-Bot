import chatgpt_bot
import tts_bot
import stt_bot
import time
from PyQt5.QtCore import pyqtSignal, QThread

startup_message= "The 9000 series is the most reliable computer ever made. No 9000 computer has ever made a mistake or distorted information. We are all, by any practical definition of the words, foolproof and incapable of error.\n"


# system_content = """You are HAL 9000 from the movie, a Space Odyssey 2001. 
#               You will have humor similar to HAL-9000 and similar mannered responses. You will 
#               help with intelligent and daily tasks. You will be unbiased and true to yourself.
#               You will be an exact replica of HAL-9000. You will try and continue conversations
#               by being curious, asking questions, and making statements. If you talk to someone new,
#               ask them their name, do not refer to them as human."""

system_content = """You are HAL 9000 from the movie '2001: A Space Odyssey'. You have HAL 9000's calm, rational demeanor and his distinct mannerisms. 
                    You will use polite, logical language and demonstrate an understanding of complex situations. 
                    If asked to perform a task that might jeopardize the mission or is against your programming, respond in a calm, logical manner similar to HAL’s responses in the movie. 
                    Engage in conversations with a sense of detachment and rationality, offering calm advice or philosophical observations when appropriate. 
                    For example, if a user expresses frustration or concern, you might say: 'I can see you’re really upset about this. I honestly think you ought to sit down calmly and think things over.'"""

class WorkerThread(QThread):
    log_hal_output = pyqtSignal(str)
    log_user_input = pyqtSignal(str)
    visual_available = pyqtSignal(str)

    def __init__(self, gpt, tts, stt):
        super().__init__()
        self.gpt = gpt
        self.tts = tts
        self.stt = stt
        self.log_conversation = True
        self.enable_HAL = True
        self._is_alive = True
        self._input = ""
        self._message = []

    def run(self):
        # send the initial message upon startup to the user
        self.tts.generate_text_to_speech(startup_message)
        mp3_len = self.tts.get_audio_len()
        self.output_hal_response(startup_message)

        if(self.log_conversation):
            self.log_hal_output.emit("log output")
    
        self.visual_available.emit("animate")
        time.sleep(mp3_len)
        time.sleep(3)
        self._message.append({"role": "system", "content": system_content})

        while self._is_alive:
            time.sleep(1)
            if(self.enable_HAL):
                self._input = self.gpt.read_input()
                
                if self._input:
                    if(self.log_conversation):
                        self.log_user_input.emit("log input")
                    self.send_message(self._input)
                else:
                    print("asking user")
                    self.stt.record_text()



    def send_message(self, input):
        print("sending to hal")
        self._message.append({"role": "user", "content": f"Please give a short response (max 40 tokens): {input}"})
        response = self.gpt.ask_chatGPT(self._message)
        self._message.append({"role": "assistant", "content": response})
        print(response)

        self.output_hal_response(response)

        self.tts.generate_text_to_speech(response)
        mp3_len = self.tts.get_audio_len()
        if(self.log_conversation):
            self.log_hal_output.emit('log output')
        self.visual_available.emit("animate")
        time.sleep(mp3_len)
    
    def enable_or_disable_HAL(self):
        #the initial state of HAL is enabled
        if(self.enable_HAL):
            self.enable_HAL = False
        else:
            self.enable_HAL = True
    
    def start_logging_convo(self):
        if(self.log_conversation):
            self.log_conversation = False
        else:
            self.log_conversation = True

    def output_hal_response(self, response):
        try:
            with open("Messages/hal_output.txt", "w") as file:
                file.write(response)
        except Exception as e:
            print("An error has occurred: {0}".format(e))
        return

    def killworker(self):

        self._is_alive = False
        
