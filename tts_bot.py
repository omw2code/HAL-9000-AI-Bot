from openai import OpenAI, APIError
import playsound
import os

class TTS():
    def __init__(self):
        self._client = OpenAI()

    def generate_text_to_speech(self, input: str) -> None:
        try:
            response = self._client.audio.speech.create(
                model="tts-1",
                voice="onyx",
                input=input
            )
            
            response.stream_to_file("output.mp3")

        except APIError as e:
            print("An error has occurred: {0}".format(e))


    # def play_audio(file_path: str) -> None:
    #     playsound.playsound(file_path)
    #     os.remove(file_path)