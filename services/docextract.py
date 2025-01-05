import re


def read_file_content(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    return content


def extract_docstring(content):
    # Use regex to extract content within triple double-quotes
    match = re.search(r'"""(.*?)"""', content, re.DOTALL)
    if match:
        return match.group(1).strip()
    raise ValueError("No Documentation contain inside the File.")


def extract_output_des(doc):
    # Extract the 'Output' section
    output_match = re.search(r'Output:\s*(.*)', doc)
    if output_match:
        return output_match.group(1).strip()
    raise ValueError("No Output contain inside the Documentation.")
