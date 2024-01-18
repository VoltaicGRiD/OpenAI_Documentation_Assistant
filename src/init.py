# Import necessary libraries
import os, time, json
import functions, creation, monitor, extensions
from openai import OpenAI
from colorama import Fore, Style
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Initialize the OpenAI client with the API key
client = OpenAI(
    api_key = os.environ.get("OPENAI_API_KEY")
)

# Create the tools
tools = creation.create_tools()

# Clear all files
extensions.clear_files(client)

extensions.clear_assistants(client)

# Add files to the assistant
files = extensions.add_files(client)

assistant = extensions.check_assistant(client)
if (assistant == None):
    assistant = creation.create_assistant(client, files, tools)
else:
    assistant = creation.modify_assistant(client, assistant.id, files, tools)

# Create a new thread and get the run ID and thread ID
run_id, thread_id = creation.create_thread(client, assistant.id, files, "Code files have been provided along with all the necessary functions and tools to complete the task. Please follow the instructions and begin.")

# Check the status of the run
run, run_step = monitor.check_status(client, run_id, thread_id)

# Run the main loop of the program
try:
    while True:
        # Check the status of the run
        run, run_step = monitor.check_status(client,run_id, thread_id)
        
        # If the step status is 'failed', print the error code and message, then break the loop
        if (run.status == "failed"):
            print(f"Error code: {Fore.CYAN}{run.last_error.code}{Style.RESET_ALL}")
            print(f"Error message: {Fore.CYAN}{run.last_error.message}{Style.RESET_ALL}")
            break
        
        # If the step status is 'requires_action', process the tool calls
        elif (run.status == "requires_action"):
            # Handle tools
            tool_outputs = extensions.tool_handling(client, files, run_step)
            
            # Submit the tool outputs
            run = monitor.submit_tool_outputs(client, thread_id, run_id, tool_outputs)
        
        # List the messages in the thread
        messages = monitor.get_messages(client, thread_id)
        
        # Get the very last message
        last_message = monitor.get_last_message(client, thread_id, messages.data[0].id)
       
        # Print the status and the last message        
        print(f'===== {Fore.GREEN}Status: {run.status}{Style.RESET_ALL} =====')
        print(f'{Fore.CYAN}{len(messages.data)}{Style.RESET_ALL} messages in thread')
        print(f'{Fore.CYAN}{len(assistant.file_ids)}{Style.RESET_ALL} files in assistant')
        print(f'{Fore.CYAN}{len(assistant.tools)}{Style.RESET_ALL} tools in assistant')
        print(f'{Fore.MAGENTA}{last_message.content[0].text.value}{Style.RESET_ALL}')
        print(f'=======================================')
            
        # Wait for 2 seconds before the next iteration
        time.sleep(5)
except KeyboardInterrupt:
    pass
    
# Output the full run and assistant objects
print(f'===== {Fore.GREEN}Run Object{Style.RESET_ALL} =====')
print(f'ID: {Fore.CYAN}{run.id}{Style.RESET_ALL}')
print(f'Status: {Fore.CYAN}{run.status}{Style.RESET_ALL}')
print(f'Started: {Fore.CYAN}{run.started_at}{Style.RESET_ALL}')
print(f'Failed: {Fore.CYAN}{run.failed_at}{Style.RESET_ALL}')
print(f'Completed: {Fore.CYAN}{run.completed_at}{Style.RESET_ALL}')
print(f'Instructions: {Fore.CYAN}{run.instructions}{Style.RESET_ALL}')
print(f'Tools: {Fore.CYAN}{run.tools}{Style.RESET_ALL}')
print(f'Files: {Fore.CYAN}{run.file_ids}{Style.RESET_ALL}')
print(f'=======================================')
print(f'===== {Fore.GREEN}Assistant Object{Style.RESET_ALL} =====')
print(f'ID: {Fore.CYAN}{assistant.id}{Style.RESET_ALL}')
print(f'Created: {Fore.CYAN}{assistant.created_at}{Style.RESET_ALL}')
print(f'Instructions: {Fore.CYAN}{assistant.instructions}{Style.RESET_ALL}')
print(f'Tools: {Fore.CYAN}{assistant.tools}{Style.RESET_ALL}')
print(f'Files: {Fore.CYAN}{assistant.file_ids}{Style.RESET_ALL}')
print(f'=======================================')

# List the messages in the thread
messages = monitor.get_messages(client, thread_id)

# If there are any messages, print the first one
last_message = monitor.get_last_message(client, thread_id, messages.data[0].id)
print(last_message.content[0].text.value)