
import os
import requests
import base64
import json
import re
from config import API_KEY, BASE_INPUT_FOLDER, BASE_PROMPT_FOLDER


MASTER_PROMPT_TEMPLATE = """Generate a photorealistic flat-lay product image of a {product_name}.

Input References:
- Image 1 (Raw Product): The ONLY source for the {product_name} structure, fabric details, and cut.
- Image 2 (Style Reference): The ONLY source for Layout, Background, Props, and Lighting.

Instructions:
1. Product Accuracy (From Image 1):
   - The {product_name} must be IDENTICAL to Image 1 with 100% accuracy.
   - Key Attributes to Preserve:
{attributes_list}
   - You MUST generate the {product_name} appearing professionally ironed and wrinkle-free, even if Image 1 has wrinkles. Remove all creases while strictly preserving the fabric texture.

2. Layout & Style (From Image 2):
   - Place the {product_name} exactly like Image 2: {layout_instruction}
   - STRICTLY MATCH Image 2's Background Surface: {background_val}
   - STRICTLY MATCH Image 2's Surrounding Props: {props_val}
   - Lighting must be soft, diffused, natural, matching Image 2's mood.

3. Configuration:
   - {product_name} detailed configuration (buttons, collar, sleeves) must match Image 1.
   - Do NOT add inner layers or undershirts.

Negative prompt:
no pattern alteration, no color change, {negative_constraints}, no stylization, no AI artifacts, wrinkles, creases, folds, messy fabric, no logo, no embroidery, no added textures, no layered clothing
"""


VARIANT_TEMPLATES = {
    "back.txt": """Generate a high-resolution flat-lay image of the BACK of the product shown in Image 1.

Input References:
- Image 1 (Generated Front): Source for BACKGROUND, LIGHTING, and STYLE.
- Image 2 (Raw Product Image): Source for REAL LIFE PRODUCT DETAILS and ANGLE.

Instructions:
1. Background & Lighting: 
   - STRICTLY MATCH Image 1. 
   - Keep the exact same background surface, lighting mood, and shadows as Image 1.
   - Do NOT use the background from Image 2.

2. Product Appearance:
   - Use Image 2 to understand how the product actually looks in real life from the back (e.g. cut, seams, yoke).
   - Use Image 1 to determine the fabric texture and color to ensure consistency with the front view.
   - The product must look like the SAME physical item as Image 1, but viewed from the back as shown in Image 2.

3. Layout:
   - Position the product centrally.

Negative prompt:
{negative_constraints}
""",
    "side.txt": """Generate a high-resolution flat-lay image of the product from Image 1, neatly FOLDED.

Input References:
- Image 1 (Generated Front): Source for BACKGROUND, LIGHTING, and STYLE.
- Image 2 (Raw Product Image): Source for REAL LIFE PRODUCT DETAILS and FOLDING STYLE.

Instructions:
1. Background & Lighting:
   - STRICTLY MATCH Image 1.
   - Keep the exact same background surface, lighting mood, and props as Image 1.

2. Product Appearance:
   - Use Image 2 to understand the folding style and visible details from this angle.
   - The fabric texture and color must EXACTLY match Image 1.
   - This determines how the product looks in real life from this specific angle/fold.

3. Layout:
   - Follow the folding arrangement shown in Image 2.
   - Ensure the fold is crisp and professional.

Negative prompt:
STRICT CONSTRAINTS: No unfolded view, no mismatched color, no bad folding, no mismatched background, {negative_constraints}
""",
    "neck.txt": """Generate a high-resolution close-up Detail Shot of the NECKLINE/COLLAR area.

Input References:
- Image 1 (Generated Front): Source for BACKGROUND, LIGHTING, and STYLE.
- Image 2 (Raw Product Image): Source for REAL LIFE PRODUCT DETAILS (Close-up).

Instructions:
1. Background & Lighting:
   - STRICTLY MATCH Image 1.
   - Even in close-up, the lighting mood and background texture must be consistent with Image 1.

2. Product Appearance:
   - Use Image 2 to see the exact construction of the neckline/collar (buttons, stitching, tags).
   - Match the fabric texture and color from Image 1.

3. Layout:
   - Zoom in on the neck area as shown in Image 2.

Negative prompt:
STRICT CONSTRAINTS: No full body view, no fuzzy details, no mismatched background, {negative_constraints}
""",
    "detail.txt": """Generate a high-resolution MACRO DETAIL Shot of the fabric/pattern.

Input References:
- Image 1 (Generated Front): Source for BACKGROUND, LIGHTING, and STYLE.
- Image 2 (Raw Product Image): Source for REAL LIFE PRODUCT DETAILS (Texture/Weave).

Instructions:
1. Background & Lighting:
   - STRICTLY MATCH Image 1's lighting mood.
   - If background is visible, it must match Image 1.

2. Product Appearance:
   - Use Image 2 to understand the fine details of the fabric (weave, print quality) in real life.
   - Match the color and general texture appearance from Image 1.

3. Layout:
   - Extreme close-up (Macro) view.

Negative prompt:
STRICT CONSTRAINTS: No full view, no conflicting patterns, no low resolution, no mismatched background, {negative_constraints}
"""
}

def analyze_with_gemini(image_path, prompt, model="gemini-3-pro-preview"):
    """
    Generic helper to analyze image with Gemini.
    """
    print(f"DEBUG: Analyze image {image_path} with model {model}")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={API_KEY}"
    headers = {"Content-Type": "application/json"}
    
    try:
        with open(image_path, "rb") as img_f:
            b64_image = base64.b64encode(img_f.read()).decode("utf-8")
            mime_type = "image/png" if image_path.lower().endswith(".png") else "image/jpeg"
    except Exception as e:
        print(f"Error reading image: {e}")
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
        response = requests.post(url, headers=headers, json=data, timeout=60)
        if response.status_code == 200:
            result = response.json()
            if "candidates" in result and result["candidates"]:
                return result["candidates"][0]["content"]["parts"][0]["text"]
            else:
                print(f"DEBUG: No candidates returned. Response: {result}")
        else:
            print(f"API Error {response.status_code}: {response.text}")
            # FALBACK LOGIC
            if response.status_code in [404, 400, 500]:
                if model != "gemini-1.5-flash":
                    print(f"DEBUG: Retrying with gemini-1.5-flash (fallback from {model})...")
                    return analyze_with_gemini(image_path, prompt, model="gemini-1.5-flash")
                
    except Exception as e:
        print(f"API Request failed: {e}")
    
    return None

def analyze_style_reference(ref_path):
    print("Analyzing Reference Style...")
    prompt = """Analyze this reference image for an e-commerce flat lay.
    Provide strictly:
    1. Layout Description (e.g., flat-lay hanging style on a wooden hanger, folded on table).
    2. Background Surface (e.g., Solid warm tan).
    3. Visible Props (e.g., Wooden hanger, sunglasses, shoes).

    Format:
    Layout: [Value]
    Background: [Value]
    Props: [Value]
    """
    return analyze_with_gemini(ref_path, prompt)

def analyze_product_features(raw_path, product_name):
    print(f"Analyzing {product_name} Key Features...")
    prompt = f"""Analyze this raw {product_name} image for manufacturing reproduction.
    1. List 5 key structural attributes that must be preserved (e.g., "Non-standard neckline", "Puff sleeves", "Smocked bodice"). Format as a line-separated list without bullets.
    2. List 5 strict negative constraints (e.g., "no collar", "no buttons", "no belt"). Format as comma-separated list.

    Format:
    Attributes:
    [Attr 1]
    [Attr 2]
    ...
    Constraints: [constraint 1, constraint 2, ...]
    """
    return analyze_with_gemini(raw_path, prompt, model="gemini-3-pro-preview")

def generate_master_prompt_content(product_name, style_data, reality_data):
    # Defaults
    layout = "flat-lay"
    bg_val = "neutral solid color"
    props_val = "none"
    attributes = f"{product_name} structure"
    constraints = "no extra items"

    # Parse Style
    if "Layout:" in style_data:
        layout = style_data.split("Layout:")[1].split("\n")[0].strip()
    if "Background:" in style_data:
        bg_val = style_data.split("Background:")[1].split("\n")[0].strip()
    if "Props:" in style_data:
        props_val = style_data.split("Props:")[1].split("\n")[0].strip()

    # Parse Reality
    if "Attributes:" in reality_data:
        # Extract block
        attr_block = reality_data.split("Attributes:")[1].split("Constraints:")[0].strip()
        attributes = attr_block # Keep newlines
    
    if "Constraints:" in reality_data:
        constraints = reality_data.split("Constraints:")[1].strip()

    return MASTER_PROMPT_TEMPLATE.format(
        product_name=product_name.lower(),
        attributes_list=attributes,
        layout_instruction=layout,
        background_val=bg_val,
        props_val=props_val,
        negative_constraints=constraints
    )

def auto_tune_prompts(product_name, reference_image_path=None):
    print(f"Starting Auto-Tune for {product_name}...")
    
    product_dir = os.path.join(BASE_INPUT_FOLDER, product_name)
    prompt_dir = os.path.join(BASE_PROMPT_FOLDER, product_name)
    
    if not os.path.exists(prompt_dir):
        os.makedirs(prompt_dir)

    # 1. Find Reference Image
    ref_image = None
    
    # Priority 0: Explicit path passed from API (Sidebar Upload)
    if reference_image_path and os.path.exists(reference_image_path):
        ref_image = reference_image_path
        print(f"Using provided reference image: {ref_image}")
    
    # Priority 1: Search in product folder
    if not ref_image and os.path.exists(product_dir):
        valid_exts = ('.png', '.jpg', '.jpeg', '.heic', '.heif')
        # Priority: explicit "reference" name
        for f in os.listdir(product_dir):
            if "reference" in f.lower() and f.lower().endswith(valid_exts):
                ref_image = os.path.join(product_dir, f)
                break
        
        # Fallback: any image
        if not ref_image:
             for f in os.listdir(product_dir):
                if f.lower().endswith(valid_exts):
                    ref_image = os.path.join(product_dir, f)
                    break

    if not ref_image:
        return "Missing Reference Image"

    # 2. Find Raw Image (First SKU)
    raw_image = None
    if os.path.exists(product_dir):
        sku_dirs = [d for d in os.listdir(product_dir) if os.path.isdir(os.path.join(product_dir, d))]
        if sku_dirs:
            first_sku = os.path.join(product_dir, sku_dirs[0])
            images = [f for f in os.listdir(first_sku) if f.lower().endswith(('.jpg', '.png', '.jpeg', '.heic', '.heif'))]
            if images:
                raw_image = os.path.join(first_sku, images[0])
    
    if not raw_image:
        return "Missing Raw Image"

    # 3. Analyze
    style_info = analyze_style_reference(ref_image)
    reality_info = analyze_product_features(raw_image, product_name)
    
    if not style_info or not reality_info:
        return "Analysis Failed"

    # 4. Generate Master Prompt
    new_master_prompt = generate_master_prompt_content(product_name, style_info, reality_info)
    
    master_path = os.path.join(prompt_dir, "master_prompt.txt")
    with open(master_path, "w", encoding="utf-8") as f:
        f.write(new_master_prompt)
    print(f"Generated new master_prompt.txt for {product_name}")

    # 5. GENERATE VARIANT PROMPTS (From Scratch using Templates)
    
    # Extract Constraints for Variants
    # We strip them to avoid duplicates if possible, but simplicity is key
    neg_constraints = "no extra items"
    if "Constraints:" in reality_info: 
        neg_constraints = reality_info.split("Constraints:")[1].strip()
    
    for filename, template in VARIANT_TEMPLATES.items():
        # Fill the template with product-specific constraints
        # Note: We don't need product_name or style in variants as they reference "Image 1"
        prompt_content = template.format(negative_constraints=neg_constraints)
        
        full_path = os.path.join(prompt_dir, filename)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(prompt_content)
        print(f"Generated {filename}")

    return "Success"

if __name__ == "__main__":
    # Test run
    auto_tune_prompts("Shirt - Flat lay")
