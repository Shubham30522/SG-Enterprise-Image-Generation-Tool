
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    print("Warning: GOOGLE_API_KEY not found in .env file.")

# OpenAI API Key (for ChatGPT / GPT Image 2)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    print("Info: OPENAI_API_KEY not found in .env file. ChatGPT image generation will be unavailable.")

# Default AI Provider: "gemini" or "chatgpt"
DEFAULT_AI_PROVIDER = os.getenv("DEFAULT_AI_PROVIDER", "gemini")

# Global Constants (Static paths)
# Chrome Automation Config
CHROME_PROFILE = os.getenv("CHROME_PROFILE", "Default")
CHROME_URL = os.getenv("CHROME_URL", "https://google.com")

# Meesho Login Credentials
MEESHO_EMAIL = os.getenv("MEESHO_EMAIL", "")
MEESHO_PASSWORD = os.getenv("MEESHO_PASSWORD", "")

# Supabase Storage Configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_BUCKET = os.getenv("SUPABASE_BUCKET", "app-storage")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("Warning: SUPABASE_URL or SUPABASE_KEY not found in .env file. Cloud storage will fail.")

# Using absolute paths to ensure reliability
BASE_INPUT_FOLDER = os.path.abspath("input_images")
BASE_PROMPT_FOLDER = os.path.abspath("Prompts")
OUTPUT_FOLDER = os.path.abspath("output_images")
