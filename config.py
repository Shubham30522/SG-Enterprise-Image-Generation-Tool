
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    print("Error: API Key not found in .env file.")
    # We don't exit here to avoid crashing imports, but main.py should handle this check.

# Global Constants (Static paths)
# Chrome Automation Config
CHROME_PROFILE = os.getenv("CHROME_PROFILE", "Default")
CHROME_URL = os.getenv("CHROME_URL", "https://google.com")

# Meesho Login Credentials
MEESHO_EMAIL = os.getenv("MEESHO_EMAIL", "")
MEESHO_PASSWORD = os.getenv("MEESHO_PASSWORD", "")

# Using absolute paths to ensure reliability
BASE_INPUT_FOLDER = os.path.abspath("input_images")
BASE_PROMPT_FOLDER = os.path.abspath("Prompts")
OUTPUT_FOLDER = os.path.abspath("output_images")
