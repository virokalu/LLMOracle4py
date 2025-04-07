import pandas as pd

file_name = 'llm_oracle_results_gemini.csv'

# Load the CSV file
df = pd.read_csv(file_name)  # Replace 'your_file.csv' with your actual file path

# Calculate the percentage of correct results
correct_count = df['LLM_correctness'].sum()
total_count = len(df)
percentage_correct = (correct_count / total_count) * 100

# Print the results
print(f"Number of correct results: {correct_count}/{total_count}")
print(f"Percentage of correct results: {percentage_correct:.2f}%")
