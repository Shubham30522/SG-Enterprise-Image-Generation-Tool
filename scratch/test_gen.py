import os, sys
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
    
    if "imagen" in model_name:
        try:
            print("Calling generate_images...", end="")
            sys.stdout.flush()
            response = client.models.generate_images(
                model=model_name,
                prompt="A simple red rose",
                config=types.GenerateImagesConfig(
                    number_of_images=1,
                    aspect_ratio="1:1"
                )
            )
            print(" -> SUCCESS!")
            sys.stdout.flush()
            return True
        except Exception as e:
            print(f" -> FAILED: {e}")
            sys.stdout.flush()
            return False
    else:
        try:
            print("Calling generate_content...", end="")
            sys.stdout.flush()
            response = client.models.generate_content(
                model=model_name,
                contents="Generate an image of a simple red rose",
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

# Test the most relevant ones: gemini-3-pro-image-preview, imagen-3.0-generate-002, and gemini-2.5-flash-image
models_to_test = [
    "gemini-3-pro-image-preview",
    "imagen-3.0-generate-002",
    "gemini-2.5-flash-image"
]

for model in models_to_test:
    test_model(model)
print("\n--- Done ---")
sys.stdout.flush()
