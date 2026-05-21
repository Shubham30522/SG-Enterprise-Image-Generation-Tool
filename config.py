
import os
import tempfile
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ─── GCP Credentials Bootstrap (Cloud Deployment) ────────────────────────
# When running on Render/Azure/etc., there is no local ADC credentials file.
# If the GCP_SERVICE_ACCOUNT_JSON env var contains the full JSON key content,
# write it to a temp file and point GOOGLE_APPLICATION_CREDENTIALS at it.
# This must run BEFORE any Google/Anthropic SDK imports.
_gcp_sa_json = os.getenv("GCP_SERVICE_ACCOUNT_JSON")
if _gcp_sa_json and not os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
    try:
        _tmp = tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", prefix="gcp_sa_", delete=False
        )
        _tmp.write(_gcp_sa_json)
        _tmp.close()
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = _tmp.name
        print(f"[GCP Auth] Service account credentials loaded from env var -> {_tmp.name}")
    except Exception as _e:
        print(f"[GCP Auth] WARNING: Failed to write service account JSON: {_e}")

# OpenAI API Key (for ChatGPT / GPT Image 2)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    print("Info: OPENAI_API_KEY not found in .env file. ChatGPT image generation will be unavailable.")

# Default AI Provider: "gemini" or "chatgpt"
DEFAULT_AI_PROVIDER = os.getenv("DEFAULT_AI_PROVIDER", "gemini")

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

if GCP_PROJECT_ID:
    # Google Auth library (used by google-genai and anthropic-vertex) requires 
    # GOOGLE_CLOUD_PROJECT env var to resolve the billing project when using 
    # user credentials (authorized_user) since they don't contain a built-in project_id.
    os.environ["GOOGLE_CLOUD_PROJECT"] = GCP_PROJECT_ID

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
