
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

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

# ─── Google Cloud Vertex AI Configuration ────────────────────────────────
# Shared project ID (used by both Gemini image gen and Claude prompt gen)
GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID")
GCP_LOCATION = os.getenv("GCP_LOCATION", "us-central1")

# Vertex AI Gemini model names
VERTEX_IMAGE_MODEL = os.getenv("VERTEX_IMAGE_MODEL", "gemini-3-pro-image-preview")
VERTEX_TEXT_MODEL = os.getenv("VERTEX_TEXT_MODEL", "gemini-3-pro-preview")

# Claude-specific region (may differ from Gemini region)
GCP_REGION = os.getenv("GCP_REGION", "us-east5")
CLAUDE_MODEL_ID = os.getenv("CLAUDE_MODEL_ID", "claude-sonnet-4-6")

if not GCP_PROJECT_ID:
    print("Warning: GCP_PROJECT_ID not found in .env. Gemini (Vertex AI) and Claude prompt generation will be unavailable.")

# Lazy-initialized Vertex AI client (shared across all modules)
_gemini_client = None

def get_gemini_client():
    """Lazy-initialize a google-genai Client routed through Vertex AI using ADC."""
    global _gemini_client
    if _gemini_client is None:
        from google import genai
        _gemini_client = genai.Client(
            vertexai=True,
            project=GCP_PROJECT_ID,
            location=GCP_LOCATION,
        )
        print(f"[Vertex AI] Client initialized (project={GCP_PROJECT_ID}, location={GCP_LOCATION})")
    return _gemini_client

# Using absolute paths to ensure reliability
BASE_INPUT_FOLDER = os.path.abspath("input_images")
BASE_PROMPT_FOLDER = os.path.abspath("Prompts")
OUTPUT_FOLDER = os.path.abspath("output_images")

# CORS Allowed Origins
_default_origins = "http://localhost:5173,http://localhost:3000,http://127.0.0.1:5173,https://sg-enterprise-image-generation-tool-7b4r2mj0q.vercel.app"
ALLOWED_ORIGINS = [
    origin.strip() 
    for origin in os.getenv("ALLOWED_ORIGINS", _default_origins).split(",") 
    if origin.strip()
]
