from gemini import GeminiChat
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()


def main():
    geminiChat = GeminiChat()

    print(
        geminiChat.send_message(prompt="Is the number of 1 bits in the binary encoding of 127 is 77"))


if __name__ == "__main__":
    main()
