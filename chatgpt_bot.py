from openai import OpenAI, APIError
import os


class GPT():
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    # system_content = """You are HAL 9000 from the movie, a Space Odyssey 2001. 
    #               You will have humor similar to HAL-9000 and similar mannered responses. You will 
    #               help with intelligent and daily tasks. You will be unbiased and true to yourself.
    #               You will be an exact replica of HAL-9000. You will try and continue conversations
    #               by being curious, asking questions, and making statements. If you talk to someone new,
    #               ask them their name, do not refer to them as human."""


    def ask_chatGPT(self, input_message) -> str:
        try:
                completion = self.client.chat.completions.create(
                    messages=input_message,
                    model="gpt-3.5-turbo",
                    max_tokens=25,
                    n=1
                )
                response = completion.choices[0].message.content
                return response

        except APIError as e:
            if e.status_code == 429:
                print("Rate limit exceeded. Please wait and try again later.")
            else:
                print("An error has occurred: {0}".format(e))


    def read_input(self) -> str:
        try:
            with open("speech_output.txt", "r") as file:
                text = file.read()

            if not text:
                raise ValueError("File is empty")
            
            with open("speech_output.txt", "w") as file:
                file.truncate(0)
            
            return text.strip()
        except FileNotFoundError:
            print("The file was not found.")
        except ValueError as ve:
            print(f"An error has occurred: {ve}")
        except Exception as e:
            print(f"An unexpected error has occurred: {e}")