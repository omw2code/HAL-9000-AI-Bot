from openai import OpenAI, APIError
from tts_bot import generate_text_to_speech
from stt_bot import record_text
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

system_content = """You are HAL 9000 from the movie, a Space Odyssey 2001. 
              You will have humor similar to HAL 9000 and similar mannered responses. You will 
              help with intelligent and daily tasks. You will be unbiased and true to yourself.
              You will be an exact replica of HAL 9000."""

system_message = [{"role": "system", "content": system_content}]
def main() -> None:
    ask_chatGPT(system_message)

    while True:
        input = read_input()
        if input:
            print("going to ask now")
            message = [{"role": "user", "content": input}]
            ask_chatGPT(message)
        else:
            print("going to record")
            record_text()


def ask_chatGPT(input_message) -> str:
    try:
            completion = client.chat.completions.create(
                messages=input_message,
                model="gpt-3.5-turbo",
                max_tokens=150,
                n=1
            )
            response = completion.choices[0].message.content
            generate_text_to_speech(response)

    except APIError as e:
        if e.status_code == 429:
            print("Rate limit exceeded. Please wait and try again later.")
        else:
            print("An error has occurred: {0}".format(e))




#TODO: refactor for genericity in an IO interface
def read_input() -> str:
    try:
        with open("speech_output.txt", "r") as file:
            text = file.readlines()
            if not text:
                raise ValueError("File is empty")
            try:
                file.seek(0)
                file.writelines(text[1:])
            except Exception as e:
                print("An error has occurred: {0}".format(e))
            finally:
                file.close()
                return text[0]
    except Exception as e:
            print("An error has occurred: {0}".format(e))


if __name__ == "__main__":
    main()
