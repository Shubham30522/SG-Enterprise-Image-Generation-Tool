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

# Test Imagen 4.0 and Imagen 4.0 Ultra
models_to_test = [
    "imagen-4.0-generate-001",
    "imagen-4.0-ultra-generate-001"
]

for model in models_to_test:
    test_model(model)
sys.stdout.flush()
