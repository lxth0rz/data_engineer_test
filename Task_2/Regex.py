# Task Title: 2. Regex
# Requirement: write a regex to process the string in rawDim to extract the height, width and the depth (as float64 integers).
# Bonus: Is there a single regex for all 5 examples ?

import os
import re
import pandas as pd

# Get current working directory
cwd = os.getcwd()

# Get the parent directory
parent_dir = os.path.abspath(os.path.join(cwd, os.pardir))

# Append the file path
file_path = os.path.join(parent_dir, "candidateEvalData", "dim_df_correct.csv")

dim_df = pd.read_csv(file_path)

patterns_dict = {'19×52cm': r"(\d+)×(\d+)×*(\d*)\s*(\w{2})",
                 "50 x 66,4 cm": r"([\d,]+)\sx\s([\d,]+)\s*([\d,]*)\s*(\w{2})",
                 "168.9 x 274.3 x 3.8 cm (66 1/2 x 108 x 1 1/2 in.)": "([\d\.]+)\sx\s([\d\.]+)\sx\s([\d\.]+)\s*(\w{2})",
                 "Sheet: 16 1/4 × 12 1/4 in. (41.3 × 31.1 cm) Image: 14 × 9 7/8 in. (35.6 × 25.1 cm)": "(\d+\.\d+)\s×\s(\d+\.\d+)\s×*\s*(\d*\.*\d*)\s*(\w{2})\)$",
                 "5 by 5in": "(\d+)\sby\s(\d+)\s*(\d*)(\w{2})",}

def inch_to_cm(inch):
    return float(inch) * 2.54

def format_dim(height, width, depth, metric_unit):

    if metric_unit == "cm":
        return float(height.replace(",", ".")), \
               float(width.replace(",", ".")), \
               float(depth.replace(",", ".")) if depth != "NaN" else depth
    elif metric_unit == "in":
        return inch_to_cm(height.replace(",", ".")), \
               inch_to_cm(width.replace(",", ".")), \
               inch_to_cm(float(depth.replace(",", "."))) if depth != "NaN" else depth

# extract_dim, one regex for each dim.
def extract_dim(raw_dim):

    # Define the regex pattern for 19×52cm
    pattern = re.compile(patterns_dict[raw_dim])

   # raw_dim = "19×52×51cm"
    # Use the search method to find the match
    match = pattern.search(raw_dim)

    # Extract the values from the match object
    if match:
        height, width, depth = format_dim(height= match.group(1),
                                          width= match.group(2),
                                          depth = match.group(3) if match.group(3) != '' else 'NaN',
                                          metric_unit = match.group(4).lower())

    else:
        print("No match found")

    # Process the string using your regex
    # ...
    # Extract the height, width, and depth as float64 integers
    # ...
    return height, width, depth

#dim_df[['height','width','depth']]=dim_df['rawDim'].apply(lambda x: extract_dim(x))

dim_df_extracted = pd.DataFrame(dim_df['rawDim'].apply(lambda x: extract_dim(x)).tolist(), columns = ['height','width','depth'])

print(dim_df_extracted.to_csv())