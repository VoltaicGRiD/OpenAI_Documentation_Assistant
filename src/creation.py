import os, json

# Define the tools
def create_tools():
    # Get the current file location
    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))

    # Open and load the JSON file into the tools list
    with open(os.path.join(__location__, 'api-function.json')) as f:
        return json.load(f)

# Create the assistant
def create_assistant(client, input_files, input_tools):
    """
    This function creates an assistant.
    
    Returns:
        assistant (object): The assistant object.
    """
   
    file_ids = []
    
    for file in input_files:
        file_ids.append(file["client_id"])
    
    # Create the assistant
    assistant = client.beta.assistants.create(
        instructions="You have been provided with various files containing code. These files may or may not contain documentation. If you feel as though the documentation in the file is already sufficient, please do not submit any documentation. Along with creating documentation, please evaluate the code to identify any issues with thread safety, and evaluate it to identify bad coding practices. If you are provided with a README file, please read it before beginning. If necessary, please update the existing README. If you are not provided with a README file, please create one. Please utilize all available functionality to complete the task.",
        name="Documentation Service Assistant",
        tools=input_tools,
        file_ids=file_ids,
        model="gpt-4-1106-preview",
    )
    
    # Return the assistant
    return assistant

def modify_assistant(client, assistant_id, input_files, input_tools):
    file_ids = []
    
    for file in input_files:
        file_ids.append(file["client_id"])
    
    # Create the assistant
    assistant = client.beta.assistants.update(
        assistant_id=assistant_id,
        tools=input_tools,
        file_ids=file_ids
    )
    
    return assistant

# Function to create a new thread
def create_thread(client,assistant_id,input_files,prompt):
    """
    This function creates a new thread and a message in that thread.
    
    Parameters:
        assistant_id (str): The ID of the assistant.
        prompt (str): The content of the message.

    Returns:
        run ID (str): The ID of the run.
        thread ID (str): The ID of the thread.
    """
    
    file_ids = []
    
    for file in input_files:
        file_ids.append(file["client_id"])
        
    # Create a new thread
    thread = client.beta.threads.create(
        messages = [
            {
                "role": "user",
                "content": prompt,
                "file_ids": file_ids
            }
        ]
    )
    
    # Run the thread
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id,
    ) 
    
    # Return the run ID and thread ID
    return run.id, thread.id