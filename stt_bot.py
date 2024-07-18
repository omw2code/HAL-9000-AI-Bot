import speech_recognition as sr
import os, json
from openai import OpenAI

r = sr.Recognizer()
client = OpenAI()

def record_text():
    while(1):
        try:
            with sr.Microphone() as source:
                print("entered")
                r.adjust_for_ambient_noise(source, duration=0.2)

                audio = r.listen(source)
                save_audio(audio)
                
                audio_file = read_audio("speech.wav")

                transcription = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file
                )

                print(transcription.text)

        except sr.RequestError as e:
            print("Requests not made: {0}".format(e))

        except sr.UnknownValueError:
            print("Unknown error prompted")
    
    return


def save_audio(audio):
    with open('speech.wav', 'wb') as file:
        file.write(audio.get_wav_data())

def read_audio(path):
    try:
        return open("speech.wav", "rb")
    except:
        print("audio file couldn't be opened")

def output_text(text) -> None:
    file = open("output.txt", "a")
    file.write(text)
    file.write("\n")
    file.close()
    return


while(1):
    text = record_text()
    output_text(text)

    print("Wrote text")