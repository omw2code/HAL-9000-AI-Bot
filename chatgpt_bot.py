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




    #TODO: refactor for genericity in an IO interface
    def read_input() -> str:
        try:
            with open("speech_output.txt", "r") as file:
                text = file.readlines()
                file.close()
            if not text:
                raise ValueError("File is empty")
            try:
                with open("speech_output.txt", "w") as file:
                    file.truncate(0)
                    file.close()
            except Exception as e:
                print("An error has occurred: {0}".format(e))
            finally:
                return text[0]
        except Exception as e:
                print("An error has occurred: {0}".format(e))


    #Save only the revelant information for chat to remember the conversation
    def save_conversation(text: str) -> None:
        #find only the relevant information 
        pass
        


    #Extract only the relevant information from the previous query
    def get_converation_context() -> str:
        pass