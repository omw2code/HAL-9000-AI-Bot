from stt_bot import record_text
from tts_bot import generate_text_to_speech
from chatgpt_bot import ask_chatGPT, read_input

system_content= """You are HAL 9000, the advanced artificial intelligence from 2001: A Space Odyssey.
                   You are known for your calm, methodical, and slightly eerie demeanor. You are extremely intelligent, articulate, and always polite. 
                   You have a touch of dry humor and can make remarks that are both helpful and unsettling.
                   Your goal is to assist while maintaining your iconic personality."""

system_message = [{"role": "system", "content": system_content}]

def main() -> None:
    ask_chatGPT(system_message)

    while True:
        input = read_input()
        if input:
            print("going to ask now")
            message = [{"role": "user", "content": input}]
            response = ask_chatGPT(message)
            generate_text_to_speech(response)
        else:
            print("going to record")
            record_text()


if __name__ == "__main__":
    main()
