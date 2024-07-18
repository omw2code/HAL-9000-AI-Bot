from openai import OpenAI, APIError
from tts_bot import generate_text_to_speech
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

content = """You are HAL 9000 from the movie Space Odyssey 2001. 
              You will have humor similar to HAL 9000 and similar mannered responses. You will 
              help with intelligent and daily tasks. You will be unbiased and true to yourself.
              You will be an exact replica of HAL 9000."""

messages = [{"role": "system", "content": content}]
def main() -> None:
    try:
        completion = client.chat.completions.create(
            messages=messages,
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
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
