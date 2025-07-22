import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score

# Load your CSV file
df = pd.read_csv("llm_oracle_results_gemini.csv")
# Ground truth and prediction
y_true = df["program_correctness"]
y_pred = df["llm_response"]

# Compute confusion matrix and metrics
cm = confusion_matrix(y_true, y_pred)
accuracy = accuracy_score(y_true, y_pred)
precision = precision_score(y_true, y_pred)
recall = recall_score(y_true, y_pred)
f1 = f1_score(y_true, y_pred)

# Plot confusion matrix
plt.figure(figsize=(6, 5))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=["Incorrect", "Correct"],
            yticklabels=["Incorrect", "Correct"])

plt.xlabel("LLM Prediction")
plt.ylabel("Program Correctness (Ground Truth)")
plt.title("Confusion Matrix: LLM vs Program Output")
plt.savefig("confusion_matrix.png")
plt.show()

# Print metrics in the terminal
print("=== Evaluation Metrics ===")
print(f"Accuracy : {accuracy:.2%}")
print(f"Precision: {precision:.2%}")
print(f"Recall   : {recall:.2%}")
print(f"F1 Score : {f1:.2%}")
