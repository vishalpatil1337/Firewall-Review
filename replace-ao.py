import pandas as pd
import os
import numpy as np
import re  # Added missing import

def load_excel_files(rules_path, firewall_path):
    """Load Excel files and perform basic validation."""
    try:
        rules_df = pd.read_excel(rules_path)
        firewall_df = pd.read_excel(firewall_path)
        
        # Validate required columns
        if 'Name' not in rules_df.columns or 'Address' not in rules_df.columns:
            raise ValueError("Rules file must contain 'Name' and 'Address' columns")
            
        return rules_df, firewall_df
    
    except Exception as e:
        print(f"Error loading files: {str(e)}")
        return None, None

def create_replacement_dict(rules_df):
    """Create a clean replacement dictionary from rules DataFrame."""
    # Drop any rows where Name or Address is null
    rules_df = rules_df.dropna(subset=['Name', 'Address'])
    
    # Convert both columns to string and strip whitespace
    rules_df['Name'] = rules_df['Name'].astype(str).str.strip()
    rules_df['Address'] = rules_df['Address'].astype(str).str.strip()
    
    # Create dictionary with exact word boundaries
    replacement_dict = dict(zip(rules_df['Name'], rules_df['Address']))
    
    # Validate the dictionary isn't empty
    if not replacement_dict:
        raise ValueError("No valid replacement rules found in rules file")
        
    return replacement_dict

def replace_words_in_cell(cell, replacement_dict):
    """Replace words in a single cell with exact matching."""
    if pd.isna(cell) or not isinstance(cell, str):
        return cell
    
    # Convert cell to string if it isn't already
    cell_str = str(cell)
    
    # Perform replacements
    for old_word, new_word in replacement_dict.items():
        # Create a regex pattern with word boundaries
        pattern = r'\b' + re.escape(old_word) + r'\b'
        cell_str = re.sub(pattern, new_word, cell_str)
    
    return cell_str

def process_firewall_data(firewall_df, replacement_dict):
    """Process the firewall DataFrame with replacements."""
    # Create a copy to avoid modifying the original
    result_df = firewall_df.copy()
    
    # Only process string/object columns
    string_columns = result_df.select_dtypes(include=['object']).columns
    
    if not len(string_columns):
        raise ValueError("No string columns found in firewall data to process")
    
    # Apply replacements to each string column
    for col in string_columns:
        result_df[col] = result_df[col].apply(lambda x: replace_words_in_cell(x, replacement_dict))
    
    return result_df

def main():
    # Get the directory of the script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Define file paths
    rules_path = os.path.join(script_dir, 'Address Objects', 'rules.xlsx')
    firewall_path = os.path.join(script_dir, 'modified_firewall.xlsx')
    output_path = os.path.join(script_dir, 'modified_firewall_updated.xlsx')
    
    # Verify files exist
    if not os.path.exists(rules_path):
        print(f"Error: Rules file not found at {rules_path}")
        return
    if not os.path.exists(firewall_path):
        print(f"Error: Firewall file not found at {firewall_path}")
        return
    
    # Load the files
    rules_df, firewall_df = load_excel_files(rules_path, firewall_path)
    if rules_df is None or firewall_df is None:
        return
    
    try:
        # Create replacement dictionary
        replacement_dict = create_replacement_dict(rules_df)
        
        # Print some information about what we're going to do
        print(f"Found {len(replacement_dict)} replacement rules")
        print(f"Processing {len(firewall_df)} rows in firewall data")
        
        # Process the firewall data
        updated_firewall_df = process_firewall_data(firewall_df, replacement_dict)
        
        # Save the results
        updated_firewall_df.to_excel(output_path, index=False)
        print(f"Successfully processed and saved to: {output_path}")
        
    except Exception as e:
        print(f"Error during processing: {str(e)}")
        raise  # Re-raise the exception for debugging purposes

if __name__ == "__main__":
    main()
