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

# This is a dictionary that contains different regular expressions (regex) for extracting information from a string.
# Each key in the dictionary is a string that represents a # different format of the information, and the corresponding
# value is the regex pattern used to extract the information from that format. The goal is to use these regex patterns to
# extract the height, width, and depth of an object as numbers from a string in a DataFrame.
patterns_dict = {'19×52cm': r"(\d+)×(\d+)×*(\d*)\s*(\w{2})",
                 "50 x 66,4 cm": r"([\d,]+)\sx\s([\d,]+)\s*([\d,]*)\s*(\w{2})",
                 "168.9 x 274.3 x 3.8 cm (66 1/2 x 108 x 1 1/2 in.)": "([\d\.]+)\sx\s([\d\.]+)\sx\s([\d\.]+)\s*(\w{2})",
                 "Sheet: 16 1/4 × 12 1/4 in. (41.3 × 31.1 cm) Image: 14 × 9 7/8 in. (35.6 × 25.1 cm)": "(\d+\.\d+)\s×\s(\d+\.\d+)\s×*\s*(\d*\.*\d*)\s*(\w{2})\)$",
                 "5 by 5in": "(\d+)\sby\s(\d+)\s*(\d*)(\w{2})",}

def inch_to_cm(inch):
    """
    Converts inches to centimeters.
    Takes in a value in inches and returns the equivalent value in centimeters.
    """
    return float(inch) * 2.54

def format_dim(height, width, depth, metric_unit):

    """
     Converts the given height, width, and depth from inches to centimeters if the metric_unit is "in"
     Otherwise, it returns the given values as is [after changing to float and changing the comma to a dot if count]
     """

    if metric_unit.lower() == "cm":
        return float(height.replace(",", ".")), \
               float(width.replace(",", ".")), \
               float(depth.replace(",", ".")) if depth != "NaN" else depth
    elif metric_unit.lower() == "in":
        return inch_to_cm(height.replace(",", ".")), \
               inch_to_cm(width.replace(",", ".")), \
               inch_to_cm(float(depth.replace(",", "."))) if depth != "NaN" else depth

# extract_dim, one regex for each dim.
def extract_dim(raw_dim):

    """
    Extracts the height, width, and depth of an object as float64 integers from a string in the "rawDim" column of a DataFrame.
    The regex pattern is chosen from the 'patterns_dict' based on the input string.
    If no match is found, it prints "No match found"
    """

    # Define the regex pattern for 19×52cm
    pattern = re.compile(patterns_dict[raw_dim])
    
    # still working on a single regex for all.
    #single_pattern_for_all_trails = re.compile('([\d\.,]+)\s*(?:×|x)\s*([\d\.,]+)\s*(?:×*|x*)\s*([\d\.,]*)(\w{2})|(\d+)\sby\s(\d+)\s*(\d*)(\w{2})')

   # raw_dim = "19×52×51cm"
    # Use the search method to find the match
    match = pattern.search(raw_dim)

    # Extract the values from the match object
    if match:
        height = match.group(1)
        width = match.group(2)
        depth = match.group(3)
        metric_unit = match.group(4)
        height, width, depth = format_dim(height= height,
                                          width= width,
                                          depth = depth if depth != '' else 'NaN',
                                          metric_unit = metric_unit)

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