import speech_recognition as sr
from openai import OpenAI, APIError
from collections import deque
class SST():
    def __init__(self):
        self._rec = sr.Recognizer()
        self._mic = sr.Microphone()
        self._client = OpenAI()
        self.historyDeque = deque(maxlen=3)
        

    def record_text(self):
        while(1):
            try:
                with self._mic  as source:
                    print("entered")
                    self._rec.adjust_for_ambient_noise(source, duration=0.2)

                    audio = self._rec.listen(source)
                    self.save_audio(audio)
                    
                    audio_file = self.read_audio()
                    try:
                        transcription = self._client.audio.transcriptions.create(
                            model="whisper-1",
                            file=audio_file
                        )
                    except APIError as e:
                        print("An error has occurred: {0}".format(e))
                    print("outputting text")

                    self.output_text(transcription.text)

                    return transcription.text
            except sr.RequestError as e:
                print("Requests not made: {0}".format(e))

            except sr.UnknownValueError:
                print("Unknown error prompted")
        
        return


    def save_audio(self, audio) -> None:
        try:
            with open('speech.wav', 'wb') as file:
                file.write(audio.get_wav_data())
        except Exception as e:
            print("An error has occurred: {0}".format(e))

        return

    def read_audio(self):
        try:
            return open("speech.wav", "rb")
        except Exception as e:
            print("An error has occurred: {0}".format(e))

        return


    def output_text(self, text) -> None:
        try:
            with open("speech_output.txt", "w") as file:
                file.write(f"New User input: {text}\n")
                file.write("Previous Conversation Context:\n")
                for i, text in enumerate(self.historyDeque):
                    file.write(f"{i + 1}: {text}\n")
        except Exception as e:
            print("An error has occurred: {0}".format(e))
        self.historyDeque.appendleft(text)
        return
