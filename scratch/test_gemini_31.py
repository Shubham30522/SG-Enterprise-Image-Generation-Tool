import sys
from google import genai
from google.genai import types

def test_model(model_name):
    print(f"\n--- Testing model: {model_name} ---")
    sys.stdout.flush()
    client = genai.Client(
        vertexai=True,
        project="project-9e6655aa-ca7e-4501-b1a",
        location="us-central1"
    )
    
    try:
        response = client.models.generate_content(
            model=model_name,
            contents="Generate an image of a red rose",
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE"],
                image_config=types.ImageConfig(
                    aspect_ratio="1:1"
                )
            )
        )
        print(" -> SUCCESS!")
        sys.stdout.flush()
        return True
    except Exception as e:
        print(f" -> FAILED: {e}")
        sys.stdout.flush()
        return False

test_model("gemini-3.1-flash-image-preview")
sys.stdout.flush()
