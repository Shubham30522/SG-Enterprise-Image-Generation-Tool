
import os
import requests
import base64
import io
from PIL import Image
from config import API_KEY, OPENAI_API_KEY

# Try to import pillow-heif for HEIC support
try:
    import pillow_heif
    pillow_heif.register_heif_opener()
    HEIC_SUPPORTED = True
except ImportError:
    HEIC_SUPPORTED = False
    print("Warning: pillow-heif not installed. HEIC files will not be supported. Install with: pip install pillow-heif")

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

def fetch_image_from_api(prompt, image_paths, aspect_ratio="1:1", image_size="1K"):
    """
    Generates an image using Gemini Pro Vision.
    image_paths: List of file paths. 
    """
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image-preview:generateContent?key={API_KEY}"
    headers = {"Content-Type": "application/json"}
    
    parts = [{"text": prompt}]
    
    # Loop through all provided image paths
    for img_path in image_paths:
        if img_path and os.path.exists(img_path):
            try:
                # Check if HEIC file
                is_heic = img_path.lower().endswith(('.heic', '.heif'))
                
                if is_heic:
                    if not HEIC_SUPPORTED:
                        print(f"Skipping HEIC file (pillow-heif not installed): {img_path}")
                        continue
                    
                    # Convert HEIC to JPEG bytes
                    image_bytes, success = convert_heic_to_jpeg_bytes(img_path)
                    if not success:
                        print(f"Failed to convert HEIC: {img_path}")
                        continue
                    mime_type = "image/jpeg"
                else:
                    # Regular image file
                    with open(img_path, "rb") as img_f:
                        image_bytes = img_f.read()
                    
                    # Determine MIME type
                    if img_path.lower().endswith(".png"):
                        mime_type = "image/png"
                    elif img_path.lower().endswith(".webp"):
                        mime_type = "image/webp"
                    else:
                        mime_type = "image/jpeg"
                
                b64_image = base64.b64encode(image_bytes).decode("utf-8")
                parts.append({
                    "inline_data": {
                        "mime_type": mime_type,
                        "data": b64_image
                    }
                })
            except Exception as e:
                print(f"Error reading image {img_path}: {e}")

    # Config
    data = {
        "contents": [{"parts": parts}],
        "generationConfig": {
            "responseModalities": ["IMAGE"],
            "imageConfig": {
                "imageSize": image_size,
                "aspectRatio": aspect_ratio 
            }
        }
    }

    try:
        print("DEBUG: Sending request to Gemini Pro Vision...") 
        response = requests.post(url, headers=headers, json=data)
        print(f"DEBUG: API Response Status: {response.status_code}") 
        
        if response.status_code == 200:
            result = response.json()
            candidate = result.get("candidates", [])[0] if result.get("candidates") else None
            if candidate and "content" in candidate:
                for part in candidate["content"].get("parts", []):
                    b64_data = part.get("inlineData", {}).get("data") or part.get("inline_data", {}).get("data")
                    if b64_data:
                        image_data = base64.b64decode(b64_data)
                        return Image.open(io.BytesIO(image_data)), None
            
            # Extract detailed error reason
            error_msg = "Unknown API Error"
            if result.get("candidates") and result["candidates"][0].get("finishReason"):
                reason = result["candidates"][0]["finishReason"]
                msg = result["candidates"][0].get("finishMessage", "No details")
                error_msg = f"{reason} - {msg}"
            
            print(f"API Warning: No image generated. {error_msg}")
            return None, error_msg

        else:
            print(f"API Error: {response.status_code} - {response.text}")
            return None, f"HTTP {response.status_code}: {response.text}"
    except Exception as e:
        print(f"API Exception: {e}")
        return None, f"Exception: {str(e)}"
    return None, "Unknown Error"

def analyze_reference_image(image_path):
    """
    Analyzes the reference image using gemini-3-pro-preview to extract Pose and Background.
    Returns a dictionary with 'Model Pose' and 'Environment Physics' texts.
    """
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-preview:generateContent?key={API_KEY}"
    headers = {"Content-Type": "application/json"}
    
    prompt = """Analyze this image and extract two specific details:
1. Model Pose: Describe the model's stance, head position, arm placement, and expression.
2. Environment Physics: Describe the background, lighting, and environment atmosphere.

Format the output exactly as follows:
Model Pose: [Description]
Environment Physics: [Description]"""

    try:
        with open(image_path, "rb") as img_f:
            b64_image = base64.b64encode(img_f.read()).decode("utf-8")
            mime_type = "image/png" if image_path.lower().endswith(".png") else "image/jpeg"
    except Exception as e:
        print(f"Error reading ref image: {e}")
        return None

    data = {
        "contents": [{
            "parts": [
                {"text": prompt},
                {"inline_data": {"mime_type": mime_type, "data": b64_image}}
            ]
        }]
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            result = response.json()
            candidate = result.get("candidates", [])[0]
            text = candidate["content"]["parts"][0]["text"]
            
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
            
        else:
            print(f"Analysis Error: {response.text}")
            return None
    except Exception as e:
        print(f"Analysis Exception: {e}")
        return None

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

def map_to_openai_size(aspect_ratio, image_size="1K"):
    # Simplified mapping to supported OpenAI sizes based on ratio and requested size
    w, h = 1024, 1024
    if aspect_ratio == "3:4":
        w, h = 768, 1024
    elif aspect_ratio == "4:3":
        w, h = 1024, 768
    elif aspect_ratio == "16:9":
        w, h = 1024, 576
    elif aspect_ratio == "9:16":
        w, h = 576, 1024
    
    if image_size == "2K":
        w, h = w * 2, h * 2
    elif image_size == "4K":
        w, h = w * 4, h * 4

    # Cap to max constraint
    if w > 3840: w = 3840
    if h > 3840: h = 3840
    
    # We construct the closest matching string. 
    # DALL-E 3 supported specific formats, but GPT-Image-2 supports flexible sizes up to 4K edges.
    return f"{w}x{h}"

def fetch_image_from_openai(prompt, image_paths, aspect_ratio="1:1", image_size="1K"):
    """
    Generates an image using OpenAI GPT Image 2.
    Same interface as fetch_image_from_api().
    Returns (PIL.Image, None) on success or (None, error_string) on failure.
    """
    if not OPENAI_API_KEY:
        return None, "OPENAI_API_KEY is not configured"
        
    try:
        from openai import OpenAI
    except ImportError:
        return None, "OpenAI Python package is not installed (pip install openai)"

    client = OpenAI(api_key=OPENAI_API_KEY)
    
    # Convert image_paths to base64 data URLs
    base64_images = []
    for img_path in image_paths:
        if img_path and os.path.exists(img_path):
            try:
                is_heic = img_path.lower().endswith(('.heic', '.heif'))
                mime_type = "image/jpeg"
                if is_heic:
                    if not HEIC_SUPPORTED:
                        print(f"Skipping HEIC file (pillow-heif not installed): {img_path}")
                        continue
                    image_bytes, success = convert_heic_to_jpeg_bytes(img_path)
                    if not success: continue
                else:
                    with open(img_path, "rb") as img_f:
                        image_bytes = img_f.read()
                    if img_path.lower().endswith(".png"):
                        mime_type = "image/png"
                    elif img_path.lower().endswith(".webp"):
                        mime_type = "image/webp"

                b64_image = base64.b64encode(image_bytes).decode("utf-8")
                base64_images.append(f"data:{mime_type};base64,{b64_image}")
            except Exception as e:
                print(f"Error processing image {img_path}: {e}")

    size_str = map_to_openai_size(aspect_ratio, image_size)
    quality_val = "low" if image_size.lower() in ("1k", "low") else "high" if image_size.lower() in ("4k", "high") else "medium"
    
    try:
        print(f"DEBUG: Sending request to OpenAI gpt-image-2 (size: {size_str}, quality: {quality_val})...")
        if len(base64_images) > 0:
            response = client.images.edit(
                model="gpt-image-2",
                image=base64_images[0], # Using the first reference image as base
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
        image_data = base64.b64decode(b64_data)
        return Image.open(io.BytesIO(image_data)), None
        
    except Exception as e:
        print(f"OpenAI API Exception: {e}")
        return None, f"OpenAI API Exception: {str(e)}"

def generate_image(prompt, image_paths, aspect_ratio="1:1", image_size="1K", provider="gemini"):
    """
    Unified entry point. Routes to the correct API based on provider.
    """
    if provider == "chatgpt":
        return fetch_image_from_openai(prompt, image_paths, aspect_ratio, image_size)
    else:
        return fetch_image_from_api(prompt, image_paths, aspect_ratio, image_size)
