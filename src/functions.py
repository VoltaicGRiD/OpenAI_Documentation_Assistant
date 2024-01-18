import os
import shutil
import uuid


def add_documentation(files, file_id, line_number, documentation):
    """
    This function adds documentation to a file at a given line number.
    
    Args:
        files (list[dict]): A list containing dictionary entries of (file_name, file_id, assistant_id) 
        file_name (str): The name of the file.
        line_number (int): The line number in the file.
        documentation (str): The documentation to add.
    """

    try:
        # Find the correct file name from the id thats provided in the dictionary of 'files'
        file_name = next(item for item in files if item["client_id"] == file_id)["full_name"]
        
        # Create the "ai_modified" directory if it doesn't exist
        if not os.path.exists("ai_modified"):
            os.makedirs("ai_modified")
        
        # Copy the original file to the "ai_modified" directory
        shutil.copy(file_name, "ai_modified")
        
        # Modify the file in the "ai_modified" directory
        modified_file_name = os.path.join("ai_modified", os.path.basename(file_name))
        with open(modified_file_name, "r") as file:
            lines = file.readlines()
            lines.insert(line_number, documentation)
        with open(modified_file_name, "w") as file:
            file.writelines(lines)
        
        print(f"Adding documentation to {file_name} at line {line_number}.")
        print(f"Documentation: {documentation}")
        print(f"Documentation added to {modified_file_name} at line {line_number}.")
        
        return "true"
    except: 
        return "false"        
    
def add_thread_safe_warning(files, file_id, line_number, documentation):
    """
    This function adds a thread safe warning to a file at a given line number.

    Args:
        files (list[dict]): A list containing dictionary entries of (file_name, file_id, assistant_id) 
        file_name (str): The name of the file.
        line_number (int): The line number in the file.
        documentation (str): The documentation to add.
    """
    
    try:        
        # Find the correct file name from the id thats provided in the dictionary of 'files'
        file_name = next(item for item in files if item["client_id"] == file_id)["full_name"]
        
        # Create the "ai_modified" directory if it doesn't exist
        if not os.path.exists("ai_modified"):
            os.makedirs("ai_modified")
        
        # Copy the original file to the "ai_modified" directory
        shutil.copy(file_name, "ai_modified")
        
        # Modify the file in the "ai_modified" directory
        modified_file_name = os.path.join("ai_modified", os.path.basename(file_name))
        with open(modified_file_name, "r") as file:
            lines = file.readlines()
            lines.insert(line_number, documentation)
        with open(modified_file_name, "w") as file:
            file.writelines(lines)
        
        print(f"Adding documentation to {file_name} at line {line_number}.")
        print(f"Documentation: {documentation}")
        print(f"Documentation added to {modified_file_name} at line {line_number}.")
        
        return "true"
    except: 
        return "false"        
    
def add_bad_practice_warning(files, file_id, line_number, documentation):
    """
    This function adds a bad practice warning to a file at a given line number.

    Args:
        files (list[dict]): A list containing dictionary entries of (file_name, file_id, assistant_id) 
        file_name (str): The name of the file.
        line_number (int): The line number in the file.
        documentation (str): The documentation to add.
    """
    
    try:        
        # Find the correct file name from the id thats provided in the dictionary of 'files'
        file_name = next(item for item in files if item["client_id"] == file_id)["full_name"]
        
        # Create the "ai_modified" directory if it doesn't exist
        if not os.path.exists("ai_modified"):
            os.makedirs("ai_modified")
        
        # Copy the original file to the "ai_modified" directory
        shutil.copy(file_name, "ai_modified")
        
        # Modify the file in the "ai_modified" directory
        modified_file_name = os.path.join("ai_modified", os.path.basename(file_name))
        with open(modified_file_name, "r") as file:
            lines = file.readlines()
            lines.insert(line_number, documentation)
        with open(modified_file_name, "w") as file:
            file.writelines(lines)
        
        print(f"Adding documentation to {file_name} at line {line_number}.")
        print(f"Documentation: {documentation}")
        print(f"Documentation added to {modified_file_name} at line {line_number}.")
        
        return "true"
    except: 
        return "false"
    
def add_readme(files, content):
    """
    This function adds a README file to the repository.
    
    Args:
        files (list[dict]): A list containing dictionary entries of (file_name, file_id, assistant_id) 
        content (str): The content of the README file.
    """
    
    try:
        # Create the "ai_modified" directory if it doesn't exist
        if not os.path.exists("ai_modified"):
            os.makedirs("ai_modified")
        
        # Check if README file already exists
        if os.path.exists("README.md"):
            # Generate a new file name
            file_name = "README_" + str(uuid.uuid4()) + ".md"
            # Create the new README file in the "ai_modified" directory
            with open(os.path.join("ai_modified", file_name), "w") as file:
                file.write(content)
            print(f"{file_name} created in the 'ai_modified' directory.")
        else:
            # Create the README file in the "ai_modified" directory
            with open(os.path.join("ai_modified", "README.md"), "w") as file:
                file.write(content)
            print("README file created in the 'ai_modified' directory.")
        return "true"
    except:
        return "false"

def replace_readme(files, content):
    """
    This function replaces the content of the README file.
    
    Args:
        files (list[dict]): A list containing dictionary entries of (file_name, file_id, assistant_id) 
        content (str): The content of the README file.
    """
    
    try:
        # Create the "ai_modified" directory if it doesn't exist
        if not os.path.exists("ai_modified"):
            os.makedirs("ai_modified")
        
        # Check if README file already exists
        if os.path.exists("README.md"):
            # Create a backup of the original README file in the "ai_modified" directory
            backup_file_name = "README_backup.md"
            shutil.copy("README.md", os.path.join("ai_modified", backup_file_name))
            print(f"Backup file '{backup_file_name}' created in the 'ai_modified' directory.")
            
            # Replace the README file in the "ai_modified" directory
            with open(os.path.join("ai_modified", "README.md"), "w") as file:
                file.write(content)
            print("README file replaced in the 'ai_modified' directory.")
            return "true" 
        else:
            print("README file does not exist.")
            return "false"
    except:
        return "false"