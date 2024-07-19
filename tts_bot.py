from openai import OpenAI
import playsound
import os


def generate_text_to_speech(input: str) -> None:

    client = OpenAI()

    try:
        response = client.audio.speech.create(
            model="tts-1",
            voice="onyx",
            input=input
        )
        
        response.stream_to_file("output.mp3")
        play_audio("output.mp3")

    except Exception as e:
        print("An error has occurred: {0}".format(e))


def play_audio(file_path: str) -> None:
    playsound.playsound(file_path)
    os.remove(file_path)