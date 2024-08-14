from openai import OpenAI, APIError
from pydub import AudioSegment
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
            
            response.stream_to_file("Audio/HAL_audio.mp3")

        except APIError as e:
            print("An error has occurred: {0}".format(e))

    def get_audio_len(self):
        try:
            audio_file = AudioSegment.from_file("Audio/HAL_audio.mp3")
            return audio_file.duration_seconds
        except FileNotFoundError as e:
            print("An error has occurred: {0}".format(e))