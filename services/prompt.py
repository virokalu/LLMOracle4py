from models.doc import Doc


def create_llm_prompt(data, output_data, input_data):
    """
    Generates an LLM prompt to verify the correctness of a function's output.

    Parameters:
    - data (dict): Contains metadata (Input descriptions, Expected Output, Example)
    - output_data (any): The actual output produced by the function
    - input_data (list): The actual inputs provided to the function

    Returns:
    - str: A formatted prompt for LLM verification
    """

    # Ensure data is a dictionary
    if isinstance(data, Doc):
        data = data.__dict__

    # Define main instruction
    prompt = (
        "We are providing all the details need to know about the function including given output, output details, "
        "inserted input and its details below. If the function is giving output as None the function is in a loop or "
        "terminated while running, Take those instances as False\n"
    )

    # Add input details and actual input values
    input_section = "We input "
    if "Input" in data:
        input_details = data["Input"]

        if isinstance(input_details, str):  # If it's a string, treat it as a single input
            input_section += f"{input_data[0]} which is {input_details}."

        elif isinstance(input_details, dict):  # If it's a dictionary, iterate over it
            for i, (key, value) in enumerate(input_details.items(), 1):
                input_value = input_data[i - 1] if i <= len(input_data) else "N/A"
                input_section += f"{input_value} which is a {value} named as {key},"
            input_section += "."

    output_section = "\nAnd the function is giving a output of "
    if "Output" in data:
        output_section += f"{output_data}, which need to be {data['Output']}.\n"

    # Combine sections to build the prompt
    prompt += f"{input_section}{output_section}"

    return prompt
