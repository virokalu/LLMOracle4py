from services.docExtract import read_file_content, extract_docstring, extract_output_des
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def main():
    # geminiChat = GeminiChat()
    #
    # print(
    #     geminiChat.send_message(prompt="Is the number of 1 bits in the binary encoding of 127 is 8"))

    file_path = 'bitcount.py'  # Replace with your .py file path
    content = extract_output_des(extract_docstring(read_file_content(file_path)))
    print(content)


if __name__ == "__main__":
    main()
