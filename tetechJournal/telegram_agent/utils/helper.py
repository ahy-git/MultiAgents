# Add your utilities or helper functions to this file.
import os
from dotenv import load_dotenv, find_dotenv

# these expect to find a .env file at the directory above the lesson.                                                                                                                     # the format for that file is (without the comment)                                                                                                                                       #API_KEYNAME=AStringThatIsTheLongAPIKeyFromSomeService                                                                                                                                     
def load_env():
    """Recursively search for a .env file in parent directories."""
    current_dir = os.getcwd()  # Start from the current working directory

    while True:
        env_path = os.path.join(current_dir, ".env")
        if os.path.exists(env_path):  # Check if .env exists in this directory
            load_dotenv(env_path)
            print(f"Loaded .env from: {env_path}")  # Debugging message
            return True  # Successfully loaded

        # Move up one directory
        parent_dir = os.path.dirname(current_dir)
        if parent_dir == current_dir:  # Stop if we reach the root directory
            print("No .env file found.")
            return False

        current_dir = parent_dir  # Update current directory to parent

def get_openai_api_key():
    load_env()
    openai_api_key = os.getenv("OPENAI_API_KEY")
    return openai_api_key
