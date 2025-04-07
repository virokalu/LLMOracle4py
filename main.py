import copy
import csv
import json
import sys
import time
from collections import deque

from dotenv import load_dotenv

from models.doc import Doc
from services.docExtract import read_file_content, extract_docstring
from services.gemini import GeminiChat
from services.handlePrograms import get_names, py_try
from services.prompt import create_llm_prompt, create_llm_prompt

# Load environment variables
load_dotenv()
MAX_CALLS = 8  # Maximum calls allowed
TIME_WINDOW = 60  # Time window in seconds (1 minute)
timestamps = deque()  # Store timestamps of API calls

""" To store results """
# Initialize data collection list
results_data = []


def main():
    # Define main instructions
    # instructions = (
    #     "You are a Test Oracle that verifies the correctness of a function's output. Your task is to check whether "
    #     "the actual output of a function is correct using the given function description. Return only 'True' if the "
    #     "output is correct and 'False' if it is incorrect. Start by understanding the function’s purpose, "
    #     "input requirements, and expected behavior. Analyze the given inputs, ensuring they match the expected format "
    #     "and constraints. Execute the function and compare its actual output with the expected output, identifying "
    #     "whether it matches, contains errors, or deviates unexpectedly. Handle edge cases by testing valid, boundary, "
    #     "and invalid inputs, observing if the function crashes, loops infinitely, or produces incorrect values. If "
    #     "the function returns None, consider whether it is stuck in a loop or failed to execute.\n"
    #     "Ensure that the response field is either True or False, indicating whether the function output is correct or "
    #     "incorrect."
    #     """
    #     Provide your response using the following format:
    #     {
    #       "properties": {
    #         "response": {
    #           "type": "boolean"
    #         },
    #         "suggestions": {
    #           "type": "string"
    #         },
    #         "reasons": {
    #           "type": "string"
    #         }
    #       },
    #       "required": ["response"]
    #     }
    #     """
    #     "Provide reasons explaining why the output is correct or incorrect and suggestions on how to improve the "
    #     "function’s correctness."
    # )

    chat = GeminiChat()

    program_path = "QuixBugs"
    py_path = "python_programs"
    test_path = "json_testcases"

    # Get the names of the programs that testcases are available
    programs_names = get_names(program_path + "/json_testcases")
    # programs_names = ['bitcount']
    # print(programs_names)

    for program_name in programs_names:
        print(f"\n{program_name}")

        """ To store results """
        # Initialize data dictionary for this program
        program_data = {
            'program_name': program_name,
            'test_cases': []
        }

        """ Getting TestCases """
        # num_lines, content = get_inputs(program_path + "/" + test_path + "/" + program_name + ".json")
        working_file = open(program_path + "/" + test_path + "/" + program_name + ".json", 'r')

        """ Read File Content """
        doc_content = extract_docstring(read_file_content(program_path + "/" + py_path + "/" + program_name + ".py"))

        """ Extract the prompt Items """
        doc = Doc(doc_content)

        print("==================================================================================")

        for line in working_file:

            current_time = time.time()
            while timestamps and timestamps[0] < current_time - TIME_WINDOW:
                timestamps.popleft()

            py_testcase = json.loads(line)
            input_, output_ = py_testcase  # Extract input and output elements
            if not isinstance(input_, list):
                input_ = [input_]

            # if isinstance(input_, list) and len(input_) == 1 and isinstance(input_[0], list):
            #     input_ = input_[0]  # Extract the single item

            """ Running the Program """
            output, error = py_try(program_name, program_path + "." + py_path, *copy.deepcopy(input_))

            # print(type(output))
            print("Input of program " + program_name + " ------------------------> " + str(input_))
            print("Output of program " + program_name + " ------------------------> " + str(output))

            if error is not None:
                print("Error on program " + program_name + " ------------------------>! " + error)
            print("\n")

            """ Prompt Creation """
            # prompt = create_llm_prompt(doc.sections, output, input_, error)
            prompt = create_llm_prompt(doc.sections, output, input_, error)
            print(prompt)

            if len(timestamps) < MAX_CALLS:

                """ Send the Prompt to the Model """
                message = chat.send_message(prompt)
                print(message)

                """ To store results """
                # Create test case data dictionary
                test_case_data = {
                    'input': str(input_),
                    'expected_output': str(output_),
                    'program_output': str(output),
                    'error': str(error) if error else None,
                    'prompt': prompt,
                    'llm_response': message
                }
                # Add test case data to program data
                program_data['test_cases'].append(test_case_data)

                timestamps.append(current_time)

            else:
                sleep_time = TIME_WINDOW - (current_time - timestamps[0])
                print(f"Rate limit reached! Sleeping for {sleep_time:.2f} seconds...")
                time.sleep(sleep_time)

                # After sleep, clear ALL expired timestamps (not just one)
                current_time = time.time()  # Update time after sleep
                while timestamps and timestamps[0] < current_time - TIME_WINDOW:
                    timestamps.popleft()

                """ Send the Prompt to the Model """
                message = chat.send_message(prompt)
                print(message)

                """ To store results """
                # Create test case data dictionary
                test_case_data = {
                    'input': str(input_),
                    'expected_output': str(output_),
                    'program_output': str(output),
                    'error': str(error) if error else None,
                    'prompt': prompt,
                    'llm_response': message
                }
                # Add test case data to program data
                program_data['test_cases'].append(test_case_data)

                timestamps.append(current_time)

        """ To store results """
        # Add program data to results
        results_data.append(program_data)

    """ To store results """
    # Save results to CSV after all programs are processed
    # csv_file = 'llm_oracle_results_gemini.csv'
    csv_file = 'llm_oracle_results_gemini.csv'

    with open(csv_file, 'w', newline='') as csvfile:
        fieldnames = [
            'program_name',
            'test_case_number',
            'input',
            'expected_output',
            'program_output',
            'error',
            'prompt',
            'llm_response',
            'llm_reasons',  # The "reasons" field
            'llm_suggestions'  # The "suggestions" field
        ]

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for program in results_data:
            for i, test_case in enumerate(program['test_cases']):

                try:
                    response_json = json.loads(test_case.get('llm_response', ''))
                    llm_response = response_json.get("response", "")
                    llm_reasons = response_json.get("reasons", "")
                    llm_suggestions = response_json.get("suggestions", "")
                except json.JSONDecodeError:
                    # Handle case where response isn't valid JSON
                    llm_response = 'ERROR'
                    llm_reasons = 'Invalid JSON response'
                    llm_suggestions = ''

                row = {
                    'program_name': program['program_name'],
                    'test_case_number': i + 1,
                    'input': test_case['input'],
                    'expected_output': test_case['expected_output'],
                    'program_output': test_case['program_output'],
                    'error': test_case['error'],
                    'prompt': test_case['prompt'],
                    'llm_response': llm_response,
                    'llm_reasons': llm_reasons,
                    'llm_suggestions': llm_suggestions,
                }
                writer.writerow(row)

    print(f"\nResults saved to {csv_file}")
    exit_program()


def exit_program():
    print("Exiting the program...")
    sys.exit()


if __name__ == "__main__":
    main()
