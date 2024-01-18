# Import necessary libraries
import os
from openai import OpenAI
import time
import json
from colorama import Fore, Style
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Initialize the OpenAI client with the API key
client = OpenAI(
    api_key = os.environ.get("OPENAI_API_KEY")
)

# Define the tools
def create_tools():
    # Get the current file location
    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))

    # Open and load the JSON file into the tools list
    with open(os.path.join(__location__, 'api-function.json')) as f:
        return json.load(f)

tools = create_tools()

# Create the assistant
def create_assistant():
    """
    This function creates an assistant.
    
    Returns:
    object: The assistant object.
    """
    
    # Create the assistant
    assistant = client.beta.assistants.create(
        instructions=
        """
        You will be given one or more files of code along with tools and functions to use to submit your documentation. If you feel as though the documentation in the file is already sufficient, please do not submit any documentation.
        Along with creating documentation, please evaluate the code to identify any issues with thread safety, and evaluate it to identify bad coding practices.
        If you are provided with a README file, please read it before beginning. If necessary, please update the existing README. If you are not provided with a README file, please create one.
        Please utilize all available functionality to complete the task.
        """,
        name="Documentation Service Assistant",
        tools=tools,
        model="gpt-4",
    )
    
    # Return the assistant
    return assistant

assistant = create_assistant()

# Define a class for functions
class FunctionsClass:
    @staticmethod
    def add_documentation(file_name, line_number, documentation):
        """
        This function adds documentation to a specified file at a specified line number.
        
        Parameters:
        file_name (str): The name of the file.
        line_number (int): The line number in the file.
        documentation (str): The documentation to add.
        """
        # Print the file name, line number, and documentation
        print(f"Adding documentation to {file_name} at line {line_number}.")
        print(f"Documentation: {documentation}")

        # with open(file_name, "r") as file:
            # lines = file.readlines()
            # lines.insert(line_number, documentation)
        # with open(file_name, "w") as file:
            # file.writelines(lines)
        # print(f"Documentation added to {file_name} at line {line_number}."


# Function to create a new thread
def create_thread(assistant_id, prompt):
    """
    This function creates a new thread and a message in that thread.
    
    Parameters:
    assistant_id (str): The ID of the assistant.
    prompt (str): The content of the message.

    Returns:
    tuple: The ID of the run and the ID of the thread.
    """
    
    # Create a new thread
    thread = client.beta.threads.create()
    my_thread_id = thread.id
    
    # Create a message in the thread
    message = client.beta.threads.messages.create(
        thread_id=my_thread_id,
        role="user",
        content=prompt
    )
    
    # Run the thread
    run = client.beta.threads.runs.create(
        thread_id=my_thread_id,
        assistant_id=assistant_id,
    ) 
    
    # Return the run ID and thread ID
    return run.id, thread.id

# Function to check the status of a run
def check_status(run_id,thread_id):
    """
    This function retrieves the status of a run.
    
    Parameters:
    run_id (str): The ID of the run.
    thread_id (str): The ID of the thread.

    Returns:
    object: The run object.
    """
    
    # Retrieve the run
    run = client.beta.threads.runs.retrieve(
        thread_id=thread_id,
        run_id=run_id
    )
    
    list_run_steps = client.beta.threads.runs.steps.list(
        thread_id=thread_id,
        run_id=run_id
    )
    
    if (len(list_run_steps.data) == 0):
        return run.status, None, None
    
    run_step = client.beta.threads.runs.steps.retrieve(
        thread_id=thread_id,
        run_id=run_id,
        step_id=list_run_steps.data[0].id
    )
    
    # Return the run
    return run.status, run_step.step_details, run_step.last_error

# Function to clear files
def clear_files():
    """
    This function retrieves all files and deletes them.
    """
    # Get the list of files
    files = client.files.list()
    
    # Loop through each file and delete it
    for file in files.data:
        print(f'Deleting file: {file.id}')
        client.files.delete(file.id)

# Call the function to clear files
clear_files()

# Initialize empty lists for files and file IDs
files = []
file_ids = []

# Prompt the user to provide a file path
response = input("Provide the path of a file (type 'exit' to exit): ")

# Loop until the user types 'exit' or an empty string
while (response != "exit" and response != ""):
    # Create a file from the provided path
    fileUpload = client.files.create(file = open(response, "rb"), purpose = 'assistants')
    
    # Add the uploaded file to the files list
    files.append(fileUpload)   
    print(f"File '{response}' uploaded successfully.")
    
    # Ask for another file path
    response = input("Provide the path of a file (type 'exit' to exit): ")

# Loop through each file in the files list
for file in files:
    # Append the file to the assistant
    file_input = client.beta.assistants.files.create(assistant.id, file_id = file.id)
    print(f'File appended to assistant: {file_input.id}')
    print(f'Original file id: {file.id}')
    
    # Add the file ID to the file_ids list
    file_ids.append(file.id)    

# Create a new thread and get the run ID and thread ID
my_run_id, my_thread_id = create_thread(assistant.id, "Please follow your instructions on the provided file(s).")

# Check the status of the run
status, step_details, last_error = check_status(my_run_id,my_thread_id)

# Loop until the step status is either 'completed' or 'failed'
while True:
    try:
        # Check the status of the run
        status, step_details, last_error = check_status(my_run_id,my_thread_id)
        
        # If the step status is 'failed', print the error code and message, then break the loop
        if (status == "failed"):
            print(f"Error code: {Fore.CYAN}{last_error.code}{Style.RESET_ALL}")
            print(f"Error message: {Fore.CYAN}{last_error.message}{Style.RESET_ALL}")
            break
        
        # If the step status is 'requires_action', process the tool calls
        elif (status == "requires_action"):
            # Initialize an empty list for calls
            calls = []  
            
            # Loop through each tool call in the step details
            for call in step_details.tool_calls:
                # Add the call to the calls list
                calls.append(call)
                
                # Print the function name and arguments
                print(f"Function: {Fore.CYAN}{ call.function.name }{Style.RESET_ALL}")
                print(f"Arguments: {Fore.CYAN}{ call.function.arguments }{Style.RESET_ALL}") 
                
            # Initialize an empty list for tool outputs
            tool_outputs = []
            
            # Loop through each call in the calls list
            for call in calls:
                # Add the tool output to the tool outputs list
                tool_outputs.append(
                    {
                        "tool_call_id": call.id,
                        "output": "true"
                    }
                )
            
            # Submit the tool outputs
            client.beta.threads.runs.submit_tool_outputs(
                thread_id=my_thread_id,
                run_id=my_run_id,
                tool_outputs=tool_outputs
            )
        
        # List the messages in the thread
        messages = client.beta.threads.messages.list(
            thread_id=my_thread_id
        )
        
        # Get the very last message
        last_message = client.beta.threads.messages.retrieve(
            thread_id=my_thread_id,
            message_id=messages.data[0].id
        )
        
        print(f'===== {Fore.GREEN}Status: {status}{Style.RESET_ALL} =====')
        print(f'{Fore.CYAN}{len(messages.data)}{Style.RESET_ALL} messages in thread')
        print(f'{Fore.MAGENTA}{last_message.content[0].text.value}{Style.RESET_ALL}')
        print(f'=======================================')
            
        # Wait for 2 seconds before the next iteration
        time.sleep(5)
    except KeyboardInterrupt:
        break

# List the messages in the thread
response = client.beta.threads.messages.list(
  thread_id=my_thread_id
)

# If there are any messages, print the first one
if response.data:
    print(response.data[0].content[0].text.value)