import os

def create_folders_and_files():
    # Define the folder names and file names
    folders = ["Address Objects", "FW", "Groups"]
    files = ["cde.txt", "oos.txt"]
    
    # Get the current working directory
    base_path = os.getcwd()

    # Create the folders
    for folder in folders:
        folder_path = os.path.join(base_path, folder)
        try:
            os.makedirs(folder_path, exist_ok=True)
            print(f"Folder '{folder}' created successfully at {folder_path}")
        except Exception as e:
            print(f"Failed to create folder '{folder}': {e}")

    # Create the text files
    for file in files:
        file_path = os.path.join(base_path, file)
        try:
            with open(file_path, 'w') as f:
                f.write("")  # Empty content
            print(f"File '{file}' created successfully at {file_path}")
        except Exception as e:
            print(f"Failed to create file '{file}': {e}")

create_folders_and_files()
