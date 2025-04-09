import importlib
import os
import subprocess
import threading


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


def py_try(function_name, filepath, *program_input, timeout=5):
    """
    Dynamically imports and runs a function from the specified module with a timeout.

    Parameters:
        function_name (str): The name of the algorithm function to run.
        filepath (str): The module path where the function is defined.
        program_input: Arguments to pass to the function.
        timeout (int): Maximum execution time in seconds (default is 5 seconds).

    Returns:
        Tuple: (Function output or None, Error message or None).
    """
    module_name = f"{filepath}.{function_name}"

    result = [None]  # Mutable container to store function output
    error = [None]

    def target():
        try:
            module = importlib.import_module(module_name)
            result[0] = getattr(module, function_name)(*program_input)  # Run function
        except Exception as e:
            error[0] = f"Error: {e}"

    thread = threading.Thread(target=target)
    thread.start()
    thread.join(timeout)  # Wait for the function to complete within the timeout

    if thread.is_alive():  # Check if function is still running after timeout
        return None, "Error: Function execution timed out"

    return result[0], error[0]
