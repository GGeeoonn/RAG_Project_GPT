import os
import openai
import time
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Check if OPENAI_API_KEY is set
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise EnvironmentError("Error: OPENAI_API_KEY is not set in the environment. Please set it in the .env file.")

# Set OpenAI key and model
openai.api_key = openai_api_key
client = openai.OpenAI(api_key=openai.api_key)
model_name = "gpt-3.5-turbo"  # Any model from GPT series

def upload_pdfs_to_assistant(client, directory_path):
    try:
        if not os.path.exists(directory_path):
            raise FileNotFoundError(f"Error: Directory '{directory_path}' does not exist.")
        if not os.listdir(directory_path):
            raise ValueError(f"Error: Directory '{directory_path}' is empty. No files to upload.")
        
        file_ids = {}
        # Get all PDF file paths from the directory
        file_paths = [os.path.join(directory_path, file) for file in os.listdir(directory_path) if file.endswith(".pdf")]

        # Check if there are any PDFs to upload
        if not file_paths:
            raise ValueError(f"Error: No PDF files found in directory '{directory_path}'.")

        # Iterate through each file and upload
        for file_path in file_paths:
            file_name = os.path.basename(file_path)
            
            # Upload the file
            with open(file_path, "rb") as file:
                uploaded_file = client.files.create(
                    file=file,
                    purpose="assistants"
                )
                print(f"Uploaded file: {file_name} with ID: {uploaded_file.id}")
                file_ids[file_name] = uploaded_file.id

        print(f"All files have been successfully uploaded")
        return file_ids

    except Exception as e:
        print(f"Error uploading files: {e}")
        return None

def get_or_create_assistant(client, model_name, assistant_name, file_ids=None):
    if not assistant_name:
        raise ValueError("Error: 'assistant_name' is not set. Please provide a valid assistant name.")
    
    description = "AI Assistant for searching and answering questions from PDF documents"
    instructions = """
    You are an AI assistant specialized in searching and answering questions from PDF documents.
    Please find relevant information from the PDF documents to answer user questions accurately.
    Always refer to the content of the PDF documents when providing answers.
    """
    
    try:
        # List all assistants
        assistants = client.beta.assistants.list()
        
        # Delete existing assistant with the same name
        for assistant in assistants.data:
            if assistant.name == assistant_name:
                print(f"Deleting existing assistant '{assistant_name}' with ID: {assistant.id}")
                client.beta.assistants.delete(assistant.id)

        # Create new assistant with files
        assistant = client.beta.assistants.create(
            name=assistant_name,
            instructions=instructions,
            model=model_name,
            tools=[{"type": "file_search"}],
            tool_resources={"file_search": {"vector_store_ids": []}}
        )
        
        print(f"New assistant '{assistant_name}' created with ID: {assistant.id}")
        return assistant

    except Exception as e:
        print(f"Error creating assistant: {e}")
        return None

# Upload PDFs and get file IDs
file_ids = upload_pdfs_to_assistant(client, 'Upload')
if not file_ids:
    raise ValueError("No files were uploaded successfully")

# Create assistant with the uploaded files
assistant_name = "my_assistant"
assistant = get_or_create_assistant(client, model_name, assistant_name, file_ids)

if not assistant:
    raise ValueError("Failed to create assistant")

# Create thread
thread = client.beta.threads.create()

# Interact with assistant
while True:
    user_input = input("Enter your question (or type 'exit' to quit): ")
    
    if user_input.lower() == 'exit':
        print("Exiting the conversation. Goodbye!")
        break

    # Add message to thread
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_input
    )

    # Create run
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id
    )

    # Wait for run to complete
    while True:
        run_status = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )
        if run_status.status == 'completed':
            break
        elif run_status.status == 'failed':
            print("Run failed:", run_status.last_error)
            break
        time.sleep(1)

    # Get messages
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    
    # Print assistant's response
    for message in messages.data:
        if message.role == "assistant":
            print("\n" + "="*50)
            print("Assistant:")
            print("-"*50)
            print(message.content[0].text.value)
            print("="*50)
            print("\n")
            break