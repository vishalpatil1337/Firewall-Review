import pandas as pd
import os

# Define the paths to the Excel files
script_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the script
all_in_one_path = os.path.join(script_dir, 'all-in-one.xlsx')  # Path to the all-in-one.xlsx file
firewall_path = os.path.join(script_dir, 'FW', 'firewall.xlsx')  # Path to the firewall.xlsx file in the FW folder

# Read the all-in-one.xlsx file
all_in_one_df = pd.read_excel(all_in_one_path)

# Read the firewall.xlsx file
firewall_df = pd.read_excel(firewall_path)

# Create a dictionary for replacements from all-in-one.xlsx
replacement_dict = dict(zip(all_in_one_df['Row A'], all_in_one_df['Row B']))

# Function to replace words in the firewall DataFrame
def replace_words_in_firewall(df, replacements):
    for col in df.columns:
        df[col] = df[col].replace(replacements, regex=True)
    return df

# Replace words in the firewall DataFrame
modified_firewall_df = replace_words_in_firewall(firewall_df, replacement_dict)

# Save the modified firewall DataFrame back to Excel
modified_firewall_path = os.path.join(script_dir, 'modified_firewall.xlsx')  # Path to save the modified file
modified_firewall_df.to_excel(modified_firewall_path, index=False)

print(f"Modified firewall data saved to {modified_firewall_path}")
