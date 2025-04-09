import json


def get_inputs(file_path):
    """
        Reads a JSON file, counts the number of lines, and returns its content.

        Parameters:
        - file_path (str): The absolute or relative path to the JSON file.

        Returns:
        - num_lines (int): Number of lines in the file.
        - content (dict or list): The JSON content.
        """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()  # Read all lines first
            num_lines = len(lines)  # Count lines

        # Parse each line as a separate JSON object
        parsed_content = []
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()  # Remove any leading/trailing whitespace
                if line:  # Ignore empty lines
                    parsed_content.append(json.loads(line))

        return num_lines, parsed_content
    except FileNotFoundError:
        return num_lines, "Error: File not found."
    except json.JSONDecodeError as e:
        return num_lines, f"Error: Invalid JSON format. {e}"