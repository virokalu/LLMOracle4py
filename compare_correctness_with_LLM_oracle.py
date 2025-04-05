import pandas as pd

file_name = 'llm_oracle_results_gemini.csv'
# Load the CSV file
df = pd.read_csv(file_name, encoding='cp1252')

# Compare 'expected_output' and 'actual_output' and create a new column 'is_correct'
df['LLM_correctness'] = df['program_correctness'] == df['llm_response']

# Save the updated DataFrame back to the CSV file
df.to_csv(file_name, index=False)
