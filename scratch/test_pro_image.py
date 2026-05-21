import sys
from google import genai
from google.genai import types

def test_multimodal_image_gen(model_name):
    print(f"\n--- Testing multimodal image gen with: {model_name} ---")
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
        if response.candidates:
            print("Candidates returned:", len(response.candidates))
        sys.stdout.flush()
        return True
    except Exception as e:
        print(f" -> FAILED: {e}")
        sys.stdout.flush()
        return False

# Test Pro text models to see if they support image output modalities
models_to_test = [
    "gemini-2.5-pro",
    "gemini-3.1-pro-preview"
]

for model in models_to_test:
    test_multimodal_image_gen(model)
sys.stdout.flush()
