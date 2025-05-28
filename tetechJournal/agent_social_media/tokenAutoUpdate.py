import requests
import os
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API credentials
APP_ID = os.getenv("INSTAGRAM_APP_ID")
APP_SECRET = os.getenv("INSTAGRAM_APP_SECRET")
ACCESS_TOKEN = os.getenv("INSTAGRAM_API_KEY")

# API URLs
DEBUG_TOKEN_URL = f"https://graph.facebook.com/debug_token?input_token={ACCESS_TOKEN}&access_token={ACCESS_TOKEN}"
REFRESH_TOKEN_URL = f"https://graph.facebook.com/v22.0/oauth/access_token?grant_type=fb_exchange_token&client_id={APP_ID}&client_secret={APP_SECRET}&fb_exchange_token={ACCESS_TOKEN}"

ENV_FILE = ".env"  # Path to the environment file


def check_token_expiration():
    """Check when the token expires and refresh if necessary."""
    response = requests.get(DEBUG_TOKEN_URL).json()

    if "data" in response:
        expires_at = response["data"].get("expires_at")
        current_time = int(time.time())

        # Calculate remaining time (in days)
        remaining_days = (expires_at - current_time) // 86400

        print(f"🔍 Token expires in {remaining_days} days.")

        # If token expires in less than 5 days, refresh it
        if remaining_days < 5:
            refresh_token()
        else:
            print("✅ Token is still valid.")
    else:
        print("❌ Error checking token:", response)


def refresh_token():
    """Refresh the Instagram API token without overwriting other `.env` variables."""
    response = requests.get(REFRESH_TOKEN_URL).json()

    if "access_token" in response:
        new_token = response["access_token"]

        # Read the existing .env file
        env_vars = {}
        if os.path.exists(ENV_FILE):
            with open(ENV_FILE, "r", encoding="utf-8") as env_file:
                for line in env_file:
                    key, _, value = line.strip().partition("=")
                    if key:
                        env_vars[key] = value

        # Update only `INSTAGRAM_API_KEY`
        env_vars["INSTAGRAM_API_KEY"] = f'"{new_token}"'

        # Write back the updated .env file
        with open(ENV_FILE, "w", encoding="utf-8") as env_file:
            for key, value in env_vars.items():
                env_file.write(f"{key}={value}\n")

        print("✅ Token refreshed and saved without removing other keys!")
    else:
        print("❌ Error refreshing token:", response)


if __name__ == "__main__":
    check_token_expiration()
