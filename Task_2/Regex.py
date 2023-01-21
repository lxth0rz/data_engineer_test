# Task Title: 2. Regex
# Requirement: write a regex to process the string in rawDim to extract the height, width and the depth (as float64 integers).

import os
import pandas as pd

# Get current working directory
cwd = os.getcwd()

# Get the parent directory
parent_dir = os.path.abspath(os.path.join(cwd, os.pardir))

# Append the file path
file_path = os.path.join(parent_dir, "candidateEvalData", "dim_df_correct.csv")

dim_df = pd.read_csv(file_path)

print(dim_df)

