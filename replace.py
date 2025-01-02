import pandas as pd
import os
import re

# Define the paths to the Excel files
script_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the script
all_in_one_path = os.path.join(script_dir, 'all-in-one.xlsx')  # Path to the all-in-one.xlsx file
firewall_path = os.path.join(script_dir, 'FW', 'firewall.xlsx')  # Path to the firewall.xlsx file in the FW folder

# Read the all-in-one.xlsx file
try:
    all_in_one_df = pd.read_excel(all_in_one_path)
except FileNotFoundError:
    raise FileNotFoundError(f"Could not find the file: {all_in_one_path}")
except Exception as e:
    raise Exception(f"An error occurred while reading {all_in_one_path}: {e}")

# Read the firewall.xlsx file
try:
    firewall_df = pd.read_excel(firewall_path)
except FileNotFoundError:
    raise FileNotFoundError(f"Could not find the file: {firewall_path}")
except Exception as e:
    raise Exception(f"An error occurred while reading {firewall_path}: {e}")

# Ensure required columns exist in all-in-one.xlsx
if 'Row A' not in all_in_one_df.columns or 'Row B' not in all_in_one_df.columns:
    raise KeyError("Columns 'Row A' and 'Row B' are required in the all-in-one.xlsx file.")

# Escape special characters in replacement patterns to avoid regex errors
def escape_regex_patterns(replacement_dict):
    escaped_dict = {}
    for key, value in replacement_dict.items():
        try:
            # Escape special characters in keys (patterns) to make them regex-safe
            escaped_key = re.escape(str(key))
            escaped_dict[escaped_key] = str(value)
        except Exception as e:
            raise ValueError(f"Error escaping key '{key}': {e}")
    return escaped_dict

# Create a dictionary for replacements from all-in-one.xlsx
replacement_dict = dict(zip(all_in_one_df['Row A'], all_in_one_df['Row B']))
replacement_dict = escape_regex_patterns(replacement_dict)

# Function to replace words in the firewall DataFrame
def replace_words_in_firewall(df, replacements):
    for col in df.columns:
        try:
            df[col] = df[col].astype(str).replace(replacements, regex=True)
        except Exception as e:
            raise Exception(f"Error processing column '{col}': {e}")
    return df

# Replace words in the firewall DataFrame
try:
    modified_firewall_df = replace_words_in_firewall(firewall_df, replacement_dict)
except Exception as e:
    raise Exception(f"An error occurred during replacement: {e}")

# Save the modified firewall DataFrame back to Excel
modified_firewall_path = os.path.join(script_dir, 'modified_firewall.xlsx')  # Path to save the modified file
try:
    modified_firewall_df.to_excel(modified_firewall_path, index=False)
    print(f"Modified firewall data saved to {modified_firewall_path}")
except Exception as e:
    raise Exception(f"An error occurred while saving the file: {e}")
