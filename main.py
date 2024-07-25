import chatgpt_bot
import tts_bot
import stt_bot
import GUI.audio_visualizer as av
import threading, time

lock = threading.Lock()

system_content= """You are HAL 9000, the advanced artificial intelligence from 2001: A Space Odyssey.
                   You are known for your calm, methodical, and slightly eerie demeanor. You are extremely intelligent, articulate, and always polite. 
                   You have a touch of dry humor and can make remarks that are both helpful and unsettling.
                   Your goal is to assist while maintaining your iconic personality."""

system_message = [{"role": "system", "content": system_content}]

def main() -> None:
    gpt = chatgpt_bot.GPT()
    tts = tts_bot.TTS()
    stt = stt_bot.SST()
    gui = av.AudioStream("../output.mp3")
    gui.start()
    gpt.ask_chatGPT(system_message)

    while True:
        input = gpt.read_input()
        
        if input:
            message = message[{"role": "user", "content": input}]
            response = gpt.ask_chatGPT(message)
            tts.generate_text_to_speech(response)

            audio_thread = threading.Thread(target=gpt.play_audio)
            audio_thread.start()
            time.sleep(0.1)
            gui.animate()
            audio_thread.join()

        else:
            stt.record_text()


if __name__ == "__main__":
    main()
