
import os
import base64
import io
from PIL import Image
from config import (
    OPENAI_API_KEY, VERTEX_IMAGE_MODEL, VERTEX_TEXT_MODEL, get_gemini_client,
    AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_DEPLOYMENT_NAME, AZURE_OPENAI_API_VERSION
)

# Try to import pillow-heif for HEIC support
try:
    import pillow_heif
    pillow_heif.register_heif_opener()
    HEIC_SUPPORTED = True
except ImportError:
    HEIC_SUPPORTED = False
    print("Warning: pillow-heif not installed. HEIC files will not be supported. Install with: pip install pillow-heif")


# ─── Image Loading Helpers ───────────────────────────────────────────────

def _load_image_bytes(image_input):
    """
    Loads image bytes from a flexible input.
    
    Accepts:
      - str (local file path)
      - bytes (raw image data)
      - tuple of (bytes, mime_type)  e.g. (b'...', 'image/jpeg')
    
    Returns: (image_bytes, mime_type) or (None, None)
    """
    # Case 1: tuple of (bytes, mime_type) — already processed
    if isinstance(image_input, tuple):
        return image_input[0], image_input[1]
    
    # Case 2: raw bytes
    if isinstance(image_input, bytes):
        return image_input, "image/jpeg"
    
    # Case 3: string path (original behavior)
    if isinstance(image_input, str):
        if not os.path.exists(image_input):
            print(f"Warning: Image path does not exist: {image_input}")
            return None, None
        
        is_heic = image_input.lower().endswith(('.heic', '.heif'))
        
        if is_heic:
            if not HEIC_SUPPORTED:
                print(f"Skipping HEIC file (pillow-heif not installed): {image_input}")
                return None, None
            image_bytes, success = convert_heic_to_jpeg_bytes(image_input)
            if not success:
                return None, None
            return image_bytes, "image/jpeg"
        
        with open(image_input, "rb") as img_f:
            image_bytes = img_f.read()
        
        if image_input.lower().endswith(".png"):
            mime_type = "image/png"
        elif image_input.lower().endswith(".webp"):
            mime_type = "image/webp"
        else:
            mime_type = "image/jpeg"
        
        return image_bytes, mime_type
    
    return None, None


def convert_heic_to_jpeg_bytes(image_path):
    """
    Converts a HEIC image to JPEG bytes for API compatibility.
    Returns (jpeg_bytes, success_bool)
    """
    try:
        img = Image.open(image_path)
        # Convert to RGB if necessary (HEIC can have alpha channel)
        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')
        
        # Save to bytes
        buffer = io.BytesIO()
        img.save(buffer, format='JPEG', quality=100)
        buffer.seek(0)
        return buffer.read(), True
    except Exception as e:
        print(f"Error converting HEIC: {e}")
        return None, False


# ─── Gemini API (Vertex AI) ───────────────────────────────────────────────

def fetch_image_from_api(prompt, image_inputs, aspect_ratio="1:1", image_size="1K"):
    """
    Generates an image using Gemini via Vertex AI.
    image_inputs: List of image sources (file paths, bytes, or (bytes, mime) tuples).
    """
    from google.genai import types

    client = get_gemini_client()
    contents = [prompt]

    # Add all provided image inputs as Part objects
    for img_input in image_inputs:
        try:
            image_bytes, mime_type = _load_image_bytes(img_input)
            if image_bytes is None:
                continue
            contents.append(types.Part.from_bytes(data=image_bytes, mime_type=mime_type))
        except Exception as e:
            print(f"Error processing image input: {e}")

    config = types.GenerateContentConfig(
        response_modalities=["IMAGE"],
        image_config=types.ImageConfig(
            aspect_ratio=aspect_ratio,
            image_size=image_size,
        ),
    )

    try:
        print(f"DEBUG: Sending request to Gemini via Vertex AI (model={VERTEX_IMAGE_MODEL}, size={image_size})...")
        response = client.models.generate_content(
            model=VERTEX_IMAGE_MODEL,
            contents=contents,
            config=config,
        )
        print("DEBUG: Vertex AI response received.")

        if response.candidates:
            candidate = response.candidates[0]
            if candidate.content and candidate.content.parts:
                for part in candidate.content.parts:
                    if part.inline_data and part.inline_data.data:
                        return Image.open(io.BytesIO(part.inline_data.data)), None

            # Extract detailed error reason
            reason = getattr(candidate, 'finish_reason', 'UNKNOWN')
            msg = getattr(candidate, 'finish_message', 'No details')
            error_msg = f"{reason} - {msg}"
            print(f"API Warning: No image generated. {error_msg}")
            return None, error_msg

        return None, "No candidates returned"

    except Exception as e:
        print(f"API Exception: {e}")
        return None, f"Exception: {str(e)}"


# ─── Reference Image Analysis (Vertex AI) ────────────────────────────────

def analyze_reference_image(image_input):
    """
    Analyzes the reference image using Gemini via Vertex AI to extract Pose and Background.
    Accepts: file path, bytes, or (bytes, mime_type) tuple.
    Returns a dictionary with 'Model Pose' and 'Environment Physics' texts.
    """
    from google.genai import types

    client = get_gemini_client()

    prompt = """Analyze this image and extract two specific details:
1. Model Pose: Describe the model's stance, head position, arm placement, and expression.
2. Environment Physics: Describe the background, lighting, and environment atmosphere.

Format the output exactly as follows:
Model Pose: [Description]
Environment Physics: [Description]"""

    try:
        image_bytes, mime_type = _load_image_bytes(image_input)
        if image_bytes is None:
            return None
    except Exception as e:
        print(f"Error reading ref image: {e}")
        return None

    try:
        response = client.models.generate_content(
            model=VERTEX_TEXT_MODEL,
            contents=[
                prompt,
                types.Part.from_bytes(data=image_bytes, mime_type=mime_type),
            ],
        )

        if response.candidates and response.candidates[0].content.parts:
            text = response.candidates[0].content.parts[0].text

            # Simple parsing
            lines = text.split('\n')
            pose_text = ""
            env_text = ""
            current_section = None

            for line in lines:
                if "Model Pose:" in line:
                    current_section = "pose"
                    pose_text += line.split("Model Pose:", 1)[1].strip() + " "
                elif "Environment Physics:" in line:
                    current_section = "env"
                    env_text += line.split("Environment Physics:", 1)[1].strip() + " "
                elif current_section == "pose":
                    pose_text += line.strip() + " "
                elif current_section == "env":
                    env_text += line.strip() + " "

            return {"Model Pose": pose_text.strip(), "Environment Physics": env_text.strip()}

        print("Analysis Warning: No candidates returned.")
        return None
    except Exception as e:
        print(f"Analysis Exception: {e}")
        return None


# ─── Prompt Injection ────────────────────────────────────────────────────

def inject_prompt_overrides(base_prompt, overrides, inject_pose=False, inject_bg=False):
    """
    Updates base_prompt with new Pose or Environment sections.
    """
    final_prompt = base_prompt
    
    # 1. Inject Pose
    if inject_pose and overrides.get("Model Pose"):
        new_pose = f"Model Pose:\n{overrides['Model Pose']}\n"
        if "Model Pose:" in final_prompt:
            # Replace existing
            parts = final_prompt.split("Model Pose:")
            pre_pose = parts[0]
            rest = parts[1]
            if "\n\n" in rest:
                post_pose = rest.split("\n\n", 1)[1]
                final_prompt = f"{pre_pose}\n{new_pose}\n{post_pose}"
            else:
                final_prompt = f"{pre_pose}\n{new_pose}"
        else:
            # Smart Insert: After first paragraph (double newline)
            if "\n\n" in final_prompt:
                p1, p2 = final_prompt.split("\n\n", 1)
                final_prompt = f"{p1}\n\n{new_pose}\n{p2}"
            else:
                final_prompt = f"{final_prompt}\n\n{new_pose}"

    # 2. Inject Background
    if inject_bg and overrides.get("Environment Physics"):
        new_env = f"Environment Physics:\n{overrides['Environment Physics']}\n"
        if "Environment Physics:" in final_prompt:
            # Replace existing
            parts = final_prompt.split("Environment Physics:")
            pre_env = parts[0]
            rest = parts[1]
            if "\n\n" in rest:
                post_env = rest.split("\n\n", 1)[1]
                final_prompt = f"{pre_env}\n{new_env}\n{post_env}"
            else:
                final_prompt = f"{pre_env}\n{new_env}"
        else:
            # Smart Insert: Before "Lighting Logic:" or "Lens Reasoning:"
            inserted = False
            for marker in ["Lighting Logic:", "Lens Reasoning:"]:
                if marker in final_prompt:
                    p1, p2 = final_prompt.split(marker, 1)
                    final_prompt = f"{p1}{new_env}\n{marker}{p2}"
                    inserted = True
                    break
            
            if not inserted:
                final_prompt = f"{final_prompt}\n\n{new_env}"
    
    return final_prompt


# ─── OpenAI GPT Image 2 ─────────────────────────────────────────────────

def map_to_openai_size(aspect_ratio, image_size="1K"):
    """
    Map aspect ratio + quality to a valid GPT Image 2 size string.

    GPT Image 2 constraints (from OpenAI docs):
      - Both dimensions must be multiples of 16
      - Max edge < 3840 px
      - Long/short ratio ≤ 3:1
      - Total pixels: 655,360 – 8,294,400  (i.e. ~0.6 MP – ~8.3 MP)

    Quality tiers (practical pixel budgets):
      Low    → ~1 MP    (fast, cheap)
      Medium → ~4 MP    (balanced)
      High   → ~8 MP    (max fidelity)
    """
    size_key = image_size.lower()
    # Normalize: 1k/low → low, 2k/medium → medium, 4k/high → high
    if size_key in ("1k", "low"):
        tier = "low"
    elif size_key in ("2k", "medium"):
        tier = "medium"
    elif size_key in ("4k", "high"):
        tier = "high"
    else:
        tier = "low"

    # Safely curated presets — guaranteed to be multiples of 16, exactly matching ratio,
    # and strictly keeping total pixels < 8,200,000 and max edge < 3800.
    presets = {
        # ratio:  (low,         medium,       high)
        "1:1":   ("1024x1024", "2048x2048", "2816x2816"), # High is ~7.9MP
        "3:4":   ("864x1152",  "1728x2304", "2448x3264"), # High is ~7.9MP
        "4:3":   ("1152x864",  "2304x1728", "3264x2448"),
        "9:16":  ("720x1280",  "1440x2560", "2016x3584"), # High is ~7.2MP
        "16:9":  ("1280x720",  "2560x1440", "3584x2016"),
    }

    tier_idx = {"low": 0, "medium": 1, "high": 2}[tier]
    ratio = aspect_ratio if aspect_ratio in presets else "1:1"
    return presets[ratio][tier_idx]


def _openai_quality_from_size(image_size):
    """Map the UI quality/size label to GPT Image 2's quality parameter."""
    key = image_size.lower()
    if key in ("1k", "low"):
        return "low"
    elif key in ("4k", "high"):
        return "high"
    else:
        return "medium"


def fetch_image_from_openai(prompt, image_inputs, aspect_ratio="1:1", image_size="1K"):
    """
    Generates an image using OpenAI GPT Image 2 (via standard OpenAI or Azure OpenAI Service).
    Same interface as fetch_image_from_api().
    Accepts image_inputs as list of file paths, bytes, or (bytes, mime) tuples.
    Returns (PIL.Image, None) on success or (None, error_string) on failure.
    """
    # Collect raw image bytes with MIME types
    raw_images = []
    for img_input in image_inputs:
        try:
            image_bytes, mime_type = _load_image_bytes(img_input)
            if image_bytes is None:
                continue
            raw_images.append((image_bytes, mime_type))
        except Exception as e:
            print(f"Error processing image input: {e}")

    size_str = map_to_openai_size(aspect_ratio, image_size)
    quality_val = _openai_quality_from_size(image_size)

    if AZURE_OPENAI_API_KEY and AZURE_OPENAI_ENDPOINT:
        return _azure_openai_request(prompt, raw_images, size_str, quality_val)
    elif OPENAI_API_KEY:
        return _standard_openai_request(prompt, raw_images, size_str, quality_val)
    else:
        return None, "Neither AZURE_OPENAI_API_KEY nor OPENAI_API_KEY is configured"


def _azure_openai_request(prompt, raw_images, size_str, quality_val):
    """Direct REST API call to Azure OpenAI — bypasses SDK URL construction issues."""
    import requests as http

    base = AZURE_OPENAI_ENDPOINT.rstrip('/')
    deploy = AZURE_OPENAI_DEPLOYMENT_NAME
    api_ver = AZURE_OPENAI_API_VERSION
    label = f"Azure OpenAI (Deployment: {deploy})"
    headers = {"api-key": AZURE_OPENAI_API_KEY}

    try:
        if raw_images:
            # Azure /images/edits does NOT support 'response_format' — it returns
            # a URL by default.  Do NOT include response_format in form data.
            url = f"{base}/openai/deployments/{deploy}/images/edits?api-version={api_ver}"
            print(f"DEBUG: POST {url} (edit, size={size_str}, quality={quality_val})")

            img_bytes, mime = raw_images[0]
            ext = "png" if "png" in mime else "jpg"
            files = {"image": (f"input.{ext}", img_bytes, mime)}
            data = {
                "prompt": prompt,
                "size": size_str,
                "quality": quality_val,
                "n": "1",
            }
            resp = http.post(url, headers=headers, files=files, data=data, timeout=180)
        else:
            url = f"{base}/openai/deployments/{deploy}/images/generations?api-version={api_ver}"
            print(f"DEBUG: POST {url} (generate, size={size_str}, quality={quality_val})")

            payload = {
                "prompt": prompt,
                "size": size_str,
                "quality": quality_val,
                "n": 1,
                "response_format": "b64_json",
            }
            resp = http.post(url, headers=headers, json=payload, timeout=180)

        if resp.status_code != 200:
            detail = resp.text[:500]
            print(f"{label} HTTP {resp.status_code}: {detail}")
            return None, f"{label} HTTP {resp.status_code}: {detail}"

        result = resp.json()
        img_entry = result["data"][0]

        # Azure edits returns a URL; generations may return b64_json
        if "b64_json" in img_entry and img_entry["b64_json"]:
            return Image.open(io.BytesIO(base64.b64decode(img_entry["b64_json"]))), None
        elif "url" in img_entry and img_entry["url"]:
            print(f"DEBUG: Downloading generated image from Azure URL...")
            img_resp = http.get(img_entry["url"], timeout=120)
            if img_resp.status_code == 200:
                return Image.open(io.BytesIO(img_resp.content)), None
            return None, f"{label}: Failed to download image (HTTP {img_resp.status_code})"
        else:
            return None, f"{label}: Response contained neither b64_json nor url"

    except Exception as e:
        print(f"{label} Exception: {e}")
        return None, f"{label} Exception: {str(e)}"


def _standard_openai_request(prompt, raw_images, size_str, quality_val):
    """Standard OpenAI SDK request for direct OpenAI API usage."""
    try:
        from openai import OpenAI
    except ImportError:
        return None, "OpenAI Python package is not installed (pip install openai)"

    client = OpenAI(api_key=OPENAI_API_KEY)
    label = "OpenAI (gpt-image-2)"

    try:
        print(f"DEBUG: Sending request to {label} (size={size_str}, quality={quality_val})...")
        if raw_images:
            response = client.images.edit(
                model="gpt-image-2",
                image=io.BytesIO(raw_images[0][0]),
                prompt=prompt,
                n=1,
                size=size_str,
                quality=quality_val,
                response_format="b64_json"
            )
        else:
            response = client.images.generate(
                model="gpt-image-2",
                prompt=prompt,
                n=1,
                size=size_str,
                quality=quality_val,
                response_format="b64_json"
            )

        b64_data = response.data[0].b64_json
        return Image.open(io.BytesIO(base64.b64decode(b64_data))), None

    except Exception as e:
        print(f"{label} Exception: {e}")
        return None, f"{label} Exception: {str(e)}"


# ─── Unified Entry Point ────────────────────────────────────────────────

def generate_image(prompt, image_inputs, aspect_ratio="1:1", image_size="1K", provider="gemini"):
    """
    Unified entry point. Routes to the correct API based on provider.
    image_inputs: List of file paths (str), raw bytes, or (bytes, mime_type) tuples.
    """
    if provider == "chatgpt":
        return fetch_image_from_openai(prompt, image_inputs, aspect_ratio, image_size)
    else:
        return fetch_image_from_api(prompt, image_inputs, aspect_ratio, image_size)
