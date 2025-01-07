import re


def replace_n(output_text, output, input_no):
    # Check if 'n' exists as a standalone word or variable
    if re.search(r'\bn\b', output_text):  # Matches 'n' as a word
        # Replace only the standalone 'n'
        no_added_text = re.sub(r'\bn\b', str(input_no), output_text)
    else:
        raise ValueError("The text does not contain 'n' to replace.")
    # Combine original and replaced text
    combined_text = f"{no_added_text} is {output}"
    return combined_text
