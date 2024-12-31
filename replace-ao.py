import pandas as pd
import os

# Define the paths to the Excel files
script_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the script
rules_path = os.path.join(script_dir, 'Address Objects', 'rules.xlsx')  # Path to the rules.xlsx file in the Address Objects directory
modified_firewall_path = os.path.join(script_dir, 'modified_firewall.xlsx')  # Path to the modified_firewall.xlsx file

# Read the rules.xlsx file (Name and Address columns)
rules_df = pd.read_excel(rules_path)

# Read the modified_firewall.xlsx file
modified_firewall_df = pd.read_excel(modified_firewall_path)

# Print the column names to check them
print("Columns in rules.xlsx:", rules_df.columns)
print("Columns in modified_firewall.xlsx:", modified_firewall_df.columns)

# Check if 'Name' and 'Address' columns exist in rules_df
if 'Name' not in rules_df.columns or 'Address' not in rules_df.columns:
    print("Error: 'Name' or 'Address' columns not found in rules.xlsx")
else:
    # Create a dictionary for replacements from rules.xlsx
    replacement_dict = dict(zip(rules_df['Name'], rules_df['Address']))

    # Function to replace words in the modified firewall DataFrame
    def replace_words_in_firewall(df, replacements):
        for col in df.columns:
            # Apply the replacement only if the item exists in the replacement dictionary
            df[col] = df[col].replace(replacements, regex=True)
        return df

    # Replace words in the modified_firewall DataFrame using the replacement dictionary
    updated_firewall_df = replace_words_in_firewall(modified_firewall_df, replacement_dict)

    # Save the modified firewall DataFrame with a new name
    output_path = os.path.join(script_dir, 'modified_firewall_updated.xlsx')  # Path to save the updated file
    updated_firewall_df.to_excel(output_path, index=False)

    print(f"Modified firewall data saved to {output_path}")
