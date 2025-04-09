import re


class Doc:
    def __init__(self, docstring):
        self.docstring = docstring
        self.sections = self.extract_all_sections()

    def extract_all_sections(self):
        # Extract all section headers and their content
        section_pattern = r"(\w+:)\s*(.*?)(?=\n\w+:|\Z)"
        sections = re.findall(section_pattern, self.docstring, re.DOTALL)

        # Process each section
        result = {}
        for section_name, section_content in sections:
            section_name = section_name.strip(":")  # Remove trailing colon
            subsections = self.extract_subsections(section_content)

            # If subsections exist, store them as a dictionary; otherwise, store the raw content
            result[section_name] = subsections if subsections else section_content.strip()

        return result

    @staticmethod
    def extract_subsections(section_content):
        # Use regex to extract subsections
        subsection_pattern = r"(\w+):\s*(.*?)(?=\n\w+:|$)"
        subsections = re.findall(subsection_pattern, section_content, re.DOTALL)

        # Convert to a dictionary
        subsection_dict = {}
        for name, description in subsections:
            # Remove any nested subsections from the description
            cleaned_description = re.sub(r"\n\s*\w+:.*", "", description).strip()

            # Remove lines with more than two consecutive newlines
            cleaned_description = re.sub(r"\n{2,}.*", "", cleaned_description).strip()

            subsection_dict[name] = cleaned_description

            # Find all nested subsections in the description
            matches = re.findall(r"\n\s*(\w+):\s*(.*)", description)

            # Store removed subsections in a dictionary
            if matches:
                subsection_dict.update({key: value for key, value in matches})

        return subsection_dict

    def print_sections(self):
        for section_name, content in self.sections.items():
            print(f"=== {section_name} ===")
            if isinstance(content, dict):  # If the section has subsections
                for sub_name, sub_content in content.items():
                    print(f"  {sub_name} == {sub_content}")
            else:  # If the section is a single block of text
                print(f"  {content}")
            print()  # Add a blank line between sections

    def __repr__(self):
        return f"{self.sections}"
