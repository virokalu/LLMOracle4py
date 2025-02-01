import re


class Doc:
    def __init__(self, docstring):
        self.input_info = self.extract_section(docstring, "Input:")
        self.output_info = self.extract_section(docstring, "Output:")
        self.precondition_info = self.extract_section(docstring, "Precondition:")

    @staticmethod
    def extract_section(text, section_name):
        """Extracts the text under a given section header."""
        pattern = rf"{section_name}\s*(.*?)(?:\n\n|\Z)"
        match = re.search(pattern, text, re.DOTALL)
        return match.group(1).strip() if match else None

    def display_info(self):
        """Prints the extracted input and output descriptions."""
        print(f"Input:\n {self.input_info}")
        if self.precondition_info:
            print(f"Precondition:\n {self.precondition_info}")
        print(f"Output:\n {self.output_info}\n\n")
