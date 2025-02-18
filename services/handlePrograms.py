import importlib
import os
import subprocess


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


def run_program(file_path, program_input=None):
    """
    Runs a program using the given file path and returns its output.

    Parameters:
    - file_path (str): The absolute or relative path to the script.
    - program_input (str, optional): Input to be passed to the program.

    Returns:
    - output (str): The output of the program.
    - error (str): Any error message from the program.
    """
    if not os.path.isfile(file_path):
        return None, f"Error: File '{file_path}' not found to run."

    try:
        result = subprocess.run(
            ["python", file_path],
            input=program_input,  # Pass input to the script
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout, None  # Output and no error
    except subprocess.CalledProcessError as e:
        return None, e.stderr  # No output, return error message


def py_try(function_name, filepath, program_input):
    """
    Dynamically imports and runs a function from the specified module.

    Parameters:
        function_name (str): The name of the algorithm function to run.
        filepath:
        program_input: Arguments to pass to the function.

    Returns:
        The function output if successful, or an error message if an exception occurs.
    """
    module_name = f"{filepath}.{function_name}"

    try:
        module = importlib.import_module(module_name)
        function = getattr(module, function_name)
        return function(program_input), None  # Run the function with provided arguments

    except AttributeError:
        return None, f"Error: Function '{function_name}' not found in '{module_name}'."
    except ModuleNotFoundError:
        return None, f"Error: Module '{module_name}' not found."
    except Exception as e:
        return None, f"Error: {e}"  # More readable error message
