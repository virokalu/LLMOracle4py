from models.doc import Doc


def create_llm_prompt(data, output_data, input_data, error):
    """
    Generates an optimized LLM prompt to verify function correctness using advanced prompt engineering techniques.

    Parameters:
    - data (dict/Doc): Contains metadata (Input, Output, Example, Precondition)
    - output_data (any): Actual function output
    - input_data (list): Actual function inputs
    - error (str/None): Any error encountered

    Returns:
    - str: A structured prompt incorporating multiple prompt engineering techniques
    """

    # Convert Doc to dict if needed
    if isinstance(data, Doc):
        data = data.__dict__

    # Technique: Chain-of-Thought (CoT) Prompting - Provide step-by-step reasoning structure
    prompt = """You are an expert software engineer validating function behavior. Follow this reasoning process:
        1. Analyze the function's intended behavior from the specifications
        2. Examine the actual inputs provided
        3. Compare expected output with the description of the actual output
        4. Consider any preconditions
        5. Evaluate any errors
        6. Conclude with correctness assessment and reasoning
        
        Function Verification Task:
        """

    # Technique: Contextual Prompting - Provide rich context
    input_section = "INPUT ANALYSIS:\n"
    if "Input" in data:
        input_details = data["Input"]

        if isinstance(input_details, str):
            input_section += f"- Provided input: {str(input_data)}\n- Input description: {input_details}\n"
        elif isinstance(input_details, dict):
            input_section += "- Parameter details:\n"
            for i, (key, value) in enumerate(input_details.items(), 1):
                input_value = input_data[i - 1] if i <= len(input_data) else "N/A"
                input_section += f"  * {key}: {input_value} (should be {value})\n"

    # Technique: Self-consistency - Ask for verification from multiple perspectives
    output_section = "\nOUTPUT VALIDATION:\n"
    if "Output" in data:
        output_section += f"- Expected output description: {data['Output']}\n- Actual output: {output_data}\n"
        output_section += "Consider: Does this output make sense given the inputs and function purpose?\n"

    # Technique: Knowledge Generation Prompting - Ask for additional insights
    analysis_section = "\nDEEPER ANALYSIS:\n"
    if output_data is None:
        analysis_section += "- The function returned None. Possible reasons:\n"
        analysis_section += "  * Infinite loop\n  * Early termination\n  * Edge case not handled\n"

    if error is not None:
        analysis_section += f"- Error encountered: {error}\n"
        analysis_section += "  * Type of error\n  * Common causes\n  * Potential fixes\n"

    # Technique: Dynamic Prompting - Conditionally include sections
    pre_section = ""
    if "Precondition" in data:
        pre_section = "\nPRECONDITIONS:\n"
        pre_section += f"- {data['Precondition']}\n"
        pre_section += "Verify if these conditions were met before execution.\n"

    # Technique: Clear Instruction with Output Indicator
    task_section = """\nVERIFICATION TASK:
        1. First analyze whether the function behaved correctly
        2. If incorrect, identify the most likely cause
        3. Suggest specific fixes or tests to validate your hypothesis
        4. Rate confidence in your assessment (Low/Medium/High)
        
        Final Answer Format:
        {
          "properties": {
            "response": {
              "type": "boolean"
            },
            "suggestions": {
              "type": "string"
            },
            "reasons": {
              "type": "string"
            }
          },
          "required": ["response"]
        }"""

    # Combine all sections
    full_prompt = prompt + input_section + output_section + analysis_section + pre_section + task_section

    return full_prompt
