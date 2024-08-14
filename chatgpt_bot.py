from openai import OpenAI, APIError
import os




class GPT():
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


    def ask_chatGPT(self, input_message) -> str:
        try:
                completion = self.client.chat.completions.create(
                    messages=input_message,
                    model="gpt-3.5-turbo",
                    max_tokens=50,
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
            with open("Messages/user_input.txt", "r") as file:
                text = file.read()

            if not text:
                raise ValueError("File is empty")
            
            # with open("speech_output.txt", "w") as file:
            #     file.truncate(0)
            
            return text.strip()
        except FileNotFoundError:
            print("The file was not found.")
        except ValueError as ve:
            print(f"An error has occurred: {ve}")
        except Exception as e:
            print(f"An unexpected error has occurred: {e}")