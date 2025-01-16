import os


def get_names(directory_path):
    # Get a list of all files in the directory
    try:
        files = os.listdir(directory_path)
    except FileNotFoundError:
        print(f"Error: Directory '{directory_path}' not found.")
        return []

    # Filter the list to include only JSON files and remove the '.json' extension
    names = [os.path.splitext(file)[0] for file in files if file.endswith('.json')]

    return names

