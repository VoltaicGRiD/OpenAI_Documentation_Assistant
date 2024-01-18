import os
from colorama import Fore, Style
import monitor, functions

# Check if an assistant already exists
def check_assistant(client):
    """
    This function checks to see if an assistant already exists.
    """
    
    # Get the list of assistants
    assistants = client.beta.assistants.list()
    
    # Loop through each assistant
    for assistant in assistants.data:
        # Check if the assistant name matches the name in the .env file
        if (assistant.name == os.environ.get("ASSISTANT_NAME") and assistant.instructions == os.environ.get("ASSISTANT_INSTRUCTIONS") and assistant.model == os.environ.get("ASSISTANT_MODEL")):
            return assistant
        
    # Return None if no assistant is found
    return None

# Delete all assistants
def clear_assistants(client):
    assistants = client.beta.assistants.list()
    
    for assistant in assistants.data:
        client.beta.assistants.delete(assistant.id)

# Function to clear files
def clear_files(client):
    """
    This function retrieves all files and deletes them.
    """
    # Get the list of files
    files = client.files.list()
    
    # Loop through each file and delete it
    for file in files.data:
        print(f'Deleting file: {file.id}')
        client.files.delete(file.id)
        
def add_files(client):
    # Initialize empty lists for files and file IDs
    files = []
  
    # Prompt the user to select (1) File or (2) Folder
    response = input("Input the path of a file or folder to upload: ")
    
    # Loop until the user types 'exit' or an empty string
    while (response != "exit" and response != ""):
        if (os.path.isfile(response)):
            # Create a file from the provided path
            file_upload = client.files.create(file = open(os.path.join(response, file), "rb"), purpose = 'assistants')
            
            # Add the uploaded file to the files list
            files.append(
                {
                    "full_name": os.path.join(response, file),
                    "client_id": file_upload.id
                }
            )   
            print(f"File '{response}' uploaded successfully.")
        
        elif (os.path.isdir(response)):
            # Prompt the user to filter for a file type
            filter = input("Filter for a file type (e.g. '.py') or leave blank to use all files in folder: ")

            # Iterate through each file in the provided folder
            for file in os.listdir(response):
                if (filter != ""):
                    if (file.endswith(filter)):
                        # Create a file from the provided path
                        file_upload = client.files.create(file = open(os.path.join(response, file), "rb"), purpose = 'assistants')
                        
                        # Add the uploaded file to the files list
                        files.append(
                            {
                                "full_name": os.path.join(response, file),
                                "client_id": file_upload.id
                            }
                        )   
                        print(f"File '{os.path.join(response, file)}' uploaded successfully.") 
               
                else: 
                    # Create a file from the provided path
                    file_upload = client.files.create(file = open(os.path.join(response, file), "rb"), purpose = 'assistants')
                    
                    # Add the uploaded file to the files list
                    files.append(
                        {
                            "full_name": os.path.join(response, file),
                            "client_id": file_upload.id
                        }
                    )   
                    print(f"File '{os.path.join(response, file)}' uploaded successfully.")
                
        else: 
            print(f"Invalid option: {response}")
        
        # Prompt the user to select (1) File or (2) Folder
        response = input("Select (1) File or (2) Folder or ('exit' or [empty] to exit): ")
        
    return files   

def tool_handling(client, files, run_step):
    # Initialize an empty list for calls
    calls = []  
    tool_outputs = []
    
    # Loop through each tool call in the step details
    for call in run_step.step_details.tool_calls:
        # Add the call to the calls list
        calls.append(call)
        
        # Print the function name and arguments
        print(f"Function: {Fore.CYAN}{ call.function.name }{Style.RESET_ALL}")
        print(f"Arguments: {Fore.CYAN}{ call.function.arguments }{Style.RESET_ALL}") 
        
        method = getattr(functions, call.function.name)
        result = method(files, call.function.arguments)
        
        # Add the tool output to the tool outputs list
        tool_outputs.append(
            {
                "tool_call_id": call.id,
                "output": result
            }
        )
       
    return tool_outputs