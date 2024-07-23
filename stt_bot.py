import speech_recognition as sr
from openai import OpenAI

class SST():
    def __init__(self):

        self._r = sr.Recognizer()
        self._client = OpenAI()

    def record_text(self):
        while(1):
            try:
                with sr.Microphone() as source:
                    print("entered")
                    self._r.adjust_for_ambient_noise(source, duration=0.2)

                    audio = self._r.listen(source)
                    self.save_audio(audio)
                    
                    audio_file = self.read_audio()

                    transcription = self._client.audio.transcriptions.create(
                        model="whisper-1",
                        file=audio_file
                    )
                    self.output_text(transcription.text)
                    return transcription.text
            except sr.RequestError as e:
                print("Requests not made: {0}".format(e))

            except sr.UnknownValueError:
                print("Unknown error prompted")
        
        return


    def save_audio(audio) -> None:
        try:
            with open('speech.wav', 'wb') as file:
                file.write(audio.get_wav_data())
        except Exception as e:
            print("An error has occurred: {0}".format(e))

        return

    def read_audio():
        try:
            return open("speech.wav", "rb")
        except Exception as e:
            print("An error has occurred: {0}".format(e))

        return


    def output_text(text) -> None:
        try:
            file = open("speech_output.txt", "a")
            try:
                file.write(text)
            except Exception as e:
                print("An error has occurred: {0}".format(e))

            finally:
                file.close()
        except Exception as e:
            print("An error has occurred: {0}".format(e))

        return
