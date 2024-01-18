# Function to check the status of a run
def check_status(client,run_id,thread_id):
    """
    This function retrieves the status of a run.
    
    Parameters:
        run_id (str): The ID of the run.
        thread_id (str): The ID of the thread.

    Returns:
        run_status (str): The status of the run.
        run_step (object): The run step object.
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
        return run, None
    
    run_step = client.beta.threads.runs.steps.retrieve(
        thread_id=thread_id,
        run_id=run_id,
        step_id=list_run_steps.data[0].id
    )
    
    # Return the run
    return run, run_step

def get_messages(client,thread_id):
    """
    This function retrieves the messages in a thread.
    
    Parameters:
        thread_id (str): The ID of the thread.

    Returns:
        object: The messages object.
    """
    
    # Retrieve the messages
    messages = client.beta.threads.messages.list(
        thread_id=thread_id
    )
    
    # Return the messages
    return messages

def get_last_message(client,thread_id,message_id):
    """
    This function retrieves the last message in a thread.
    
    Parameters:
        thread_id (str): The ID of the thread.
        message_id (str): The ID of the message.

    Returns:
        object: The message object.
    """
    
    # Retrieve the message
    message = client.beta.threads.messages.retrieve(
        thread_id=thread_id,
        message_id=message_id
    )
    
    # Return the message
    return message

def submit_tool_outputs(client, thread_id, run_id, tool_outputs):
    """
    This function submits tool outputs for a run.
    
    Parameters:
        thread_id (str): The ID of the thread.
        run_id (str): The ID of the run.
        tool_outputs (list[dict]): A list containing dictionary entries of (tool_call_id, output).

    Returns:
        object: The run object.
    """
    
    # Submit the tool outputs
    run = client.beta.threads.runs.submit_tool_outputs(
        thread_id=thread_id,
        run_id=run_id,
        tool_outputs=tool_outputs
    )
    
    # Return the run
    return run