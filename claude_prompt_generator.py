"""
Claude Prompt Generator — Generates fashion photography prompts via Google Cloud Vertex AI.
Uses the SKILL/ai-fashion-photography-prompt-v2.md framework as the system prompt,
sends garment images + optional reference image to Claude Sonnet 4.6,
and returns structured per-angle prompts.
"""

import os
import json
import base64
import re

from config import (
    GCP_PROJECT_ID, GCP_REGION, CLAUDE_MODEL_ID,
    BASE_INPUT_FOLDER, BASE_PROMPT_FOLDER
)

# Skill file path (relative to repo root)
SKILL_FILE_PATH = os.path.join(os.path.dirname(__file__), "SKILL", "ai-fashion-photography-prompt-v2.md")

# Mapping from Claude's angle names → on-disk prompt filenames
ANGLE_TO_FILENAME = {
    "front": "master_prompt.txt",
    "back": "back.txt",
    "side": "side.txt",
    "close-up (topwear)": "neck.txt",
    "close-up topwear": "neck.txt",
    "closeup topwear": "neck.txt",
    "close-up (bottomwear)": "detail.txt",
    "close-up bottomwear": "detail.txt",
    "closeup bottomwear": "detail.txt",
    "3/4 front": "three_quarter.txt",
    "3/4 turn": "three_quarter.txt",
    "back detail": "back_detail.txt",
    "neck": "neck.txt",
    "detail": "detail.txt",
    "waistband": "waistband.txt",
}

IMAGE_EXTS = ('.png', '.jpg', '.jpeg', '.heic', '.heif', '.webp')


def _get_vertex_client():
    """Create an AnthropicVertex client."""
    from anthropic import AnthropicVertex
    return AnthropicVertex(
        project_id=GCP_PROJECT_ID,
        region=GCP_REGION,
        default_headers={"anthropic-version": "vertex-2023-10-16"}
    )


def _load_skill_file():
    """Read the skill framework markdown file."""
    if not os.path.exists(SKILL_FILE_PATH):
        raise FileNotFoundError(f"Skill file not found: {SKILL_FILE_PATH}")
    with open(SKILL_FILE_PATH, "r", encoding="utf-8") as f:
        return f.read()


def _encode_image(file_path):
    """Read an image file and return (base64_string, media_type)."""
    ext = os.path.splitext(file_path)[1].lower()
    mime_map = {
        '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg',
        '.png': 'image/png', '.webp': 'image/webp',
        '.heic': 'image/jpeg', '.heif': 'image/jpeg',
    }
    media_type = mime_map.get(ext, 'image/jpeg')
    with open(file_path, "rb") as f:
        return base64.standard_b64encode(f.read()).decode("utf-8"), media_type


def _map_angle_to_filename(angle_name):
    """Convert an angle name from Claude's output to a prompt filename."""
    normalized = angle_name.strip().lower()
    if normalized in ANGLE_TO_FILENAME:
        return ANGLE_TO_FILENAME[normalized]
    # Fallback: sanitize and create filename
    safe_name = re.sub(r'[^a-z0-9]+', '_', normalized).strip('_')
    return f"{safe_name}.txt"


def _parse_claude_response(response_text):
    """
    Parse Claude's response to extract per-angle prompts.
    Expects a JSON block with an "angles" dict.
    Falls back to regex extraction if JSON parsing fails.
    """
    # Try to extract JSON from the response
    json_match = re.search(r'```json\s*(.*?)\s*```', response_text, re.DOTALL)
    if json_match:
        try:
            data = json.loads(json_match.group(1))
            if "angles" in data:
                return data["angles"]
        except json.JSONDecodeError:
            pass

    # Try parsing the whole response as JSON
    try:
        data = json.loads(response_text)
        if "angles" in data:
            return data["angles"]
    except json.JSONDecodeError:
        pass

    # Fallback: regex-based extraction for markdown sections
    # Look for ## FRONT PROMPT, ## BACK PROMPT, etc.
    angles = {}
    pattern = r'##\s*(.+?)\s*PROMPT\s*\n(.*?)(?=##\s*\w+.*?PROMPT|\Z)'
    matches = re.findall(pattern, response_text, re.DOTALL | re.IGNORECASE)
    for angle_name, content in matches:
        clean_name = angle_name.strip()
        # Remove the "ChatGPT Upload Instructions" header if present
        content = re.sub(
            r'\*\*ChatGPT Upload Instructions:?\*\*.*?(?=\n(?:Scene:|Subject:|Photorealistic|Generate))',
            '', content, flags=re.DOTALL
        ).strip()
        if content:
            angles[clean_name] = content

    return angles


def generate_prompts_with_claude(
    product_name: str,
    sku_name: str,
    custom_instruction: str = "",
    reference_image_path: str = None,
    input_folder: str = None,
    prompt_folder: str = None,
):
    """
    Main entry point. Sends garment images + skill file to Claude via Vertex AI
    and writes the returned prompts to Prompts/<product>/.

    Returns: dict with "status", "files_written", "angles_generated"
    """
    if not GCP_PROJECT_ID:
        return {"error": "GCP Project ID not configured. Add GCP_PROJECT_ID to .env"}

    # 1. Load skill file
    try:
        skill_content = _load_skill_file()
    except FileNotFoundError as e:
        return {"error": str(e)}

    # 2. Collect garment images from SKU folder
    sku_path = os.path.join(input_folder or BASE_INPUT_FOLDER, product_name, sku_name)
    if not os.path.exists(sku_path):
        return {"error": f"SKU folder not found: {product_name}/{sku_name}"}

    garment_images = []
    for f in sorted(os.listdir(sku_path)):
        if f.lower().endswith(IMAGE_EXTS):
            full_path = os.path.join(sku_path, f)
            garment_images.append((full_path, f))

    if not garment_images:
        return {"error": f"No garment images found in {product_name}/{sku_name}. Upload at least one image first."}

    # 3. Build the message content
    user_content = []

    # Add garment images with labels
    for i, (img_path, filename) in enumerate(garment_images):
        b64_data, media_type = _encode_image(img_path)
        label = os.path.splitext(filename)[0]
        user_content.append({
            "type": "text",
            "text": f"[GARMENT IMAGE {i+1}: {label}]"
        })
        user_content.append({
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": media_type,
                "data": b64_data,
            }
        })

    # Add reference image if provided
    if reference_image_path and os.path.exists(reference_image_path):
        b64_data, media_type = _encode_image(reference_image_path)
        user_content.append({
            "type": "text",
            "text": "[REFERENCE / STYLE BACKGROUND IMAGE]"
        })
        user_content.append({
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": media_type,
                "data": b64_data,
            }
        })

    # Build the instruction text
    instruction_parts = [
        f"Product name: {product_name}",
        f"SKU / Color: {sku_name}",
        "",
        "TASK: Analyze the garment images above and generate prompts following the MULTI-ANGLE CATALOG MODE workflow from the skill framework.",
        "",
        "STEPS TO FOLLOW:",
        "1. Perform GARMENT ANALYSIS (Step 1 from the skill) on the uploaded garment images.",
        "2. Determine the BACKGROUND — if a reference background image is provided, extract its details. If not, auto-design a background using the skill's reasoning framework.",
        "3. Use the default model specification from the skill (Step 3).",
        "4. Generate prompts for Front and Back angles at minimum.",
        "5. Each prompt MUST follow the full 10-section MANDATORY PROMPT STRUCTURE (Scene, Subject, Body & Anatomy, Skin, Eyes, Garment, Accessories, Camera & Lighting, Use case, Constraints).",
        "",
        "IMPORTANT RULES:",
        "- Do NOT include any 'ChatGPT Upload Instructions' headers in the prompts.",
        "- Do NOT mention 'Image 1' or 'Image 2' references — each prompt should be self-contained and ready to use directly.",
        "- The prompts will be used with an AI image generation API that receives the garment images separately. Write prompts as standalone generation instructions.",
        "- Follow ALL catalog consistency rules from the skill.",
    ]

    if custom_instruction:
        instruction_parts.extend([
            "",
            "ADDITIONAL USER INSTRUCTIONS:",
            custom_instruction,
        ])

    instruction_parts.extend([
        "",
        "OUTPUT FORMAT: Return a JSON object wrapped in ```json``` code fences with this exact structure:",
        '{',
        '  "angles": {',
        '    "Front": "full prompt text for front view...",',
        '    "Back": "full prompt text for back view...",',
        '    "Side": "full prompt text if applicable...",',
        '    "Close-up (TopWear)": "full prompt text if applicable...",',
        '    "Close-up (BottomWear)": "full prompt text if applicable..."',
        '  }',
        '}',
        "",
        "Only include angles you determine are appropriate based on garment analysis + any user-requested angles.",
        "Front and Back are ALWAYS required.",
    ])

    user_content.append({
        "type": "text",
        "text": "\n".join(instruction_parts)
    })

    # 4. Call Claude via Vertex AI
    print(f"[Claude Vertex] Calling model {CLAUDE_MODEL_ID} in {GCP_PROJECT_ID}...")

    try:
        client = _get_vertex_client()

        response = client.messages.create(
            model=CLAUDE_MODEL_ID,
            max_tokens=8192,
            system=skill_content,
            messages=[
                {
                    "role": "user",
                    "content": user_content,
                }
            ]
        )

        response_text = response.content[0].text
        print(f"[Claude Vertex] Response received ({len(response_text)} chars)")

    except Exception as e:
        error_msg = str(e)
        print(f"[Claude Vertex] API Error: {error_msg}")
        return {"error": f"Claude API call failed: {error_msg}"}

    # 5. Parse response into per-angle prompts
    angles = _parse_claude_response(response_text)

    if not angles:
        return {
            "error": "Failed to parse Claude's response into structured prompts.",
            "raw_response": response_text[:2000],
        }

    # 6. Write prompts to disk
    prompt_dir = os.path.join(prompt_folder or BASE_PROMPT_FOLDER, product_name)
    os.makedirs(prompt_dir, exist_ok=True)

    # Clear existing prompt files before writing new ones
    for f in os.listdir(prompt_dir):
        if f.endswith('.txt'):
            os.remove(os.path.join(prompt_dir, f))

    files_written = []
    angles_generated = []

    for angle_name, prompt_content in angles.items():
        filename = _map_angle_to_filename(angle_name)
        file_path = os.path.join(prompt_dir, filename)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(prompt_content.strip())
        files_written.append(filename)
        angles_generated.append(angle_name)
        print(f"[Claude] Wrote {filename} ({len(prompt_content)} chars)")

    return {
        "status": "success",
        "files_written": files_written,
        "angles_generated": angles_generated,
        "product": product_name,
    }
