"""
Gemini Auto Tool - FastAPI Backend Server
Wraps existing Python logic (api_client, configure_prompts, utils, config)
and exposes REST + SSE endpoints for the React frontend.
"""

import os
import io
import uuid
import time
import json
import shutil
import asyncio
import zipfile
import threading
import base64
from typing import Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Query
from fastapi.responses import StreamingResponse, FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# Import existing project modules (unchanged)
from config import BASE_INPUT_FOLDER, BASE_PROMPT_FOLDER, OUTPUT_FOLDER, API_KEY
import utils
import api_client
import configure_prompts


# ─── Job State Management ───────────────────────────────────────────────

class JobState:
    """Tracks the state of a generation job (replaces Tkinter's self.current_job_id pattern)."""
    def __init__(self, job_id: str):
        self.job_id = job_id
        self.cancelled = False
        self.status = "pending"
        self.events = []  # list of SSE messages
        self.lock = threading.Lock()
        self.done_event = threading.Event()
    
    def push_event(self, event_type: str, data: dict):
        with self.lock:
            self.events.append({"type": event_type, "data": data})
    
    def cancel(self):
        self.cancelled = True
        self.done_event.set()


# Global job registry
active_jobs: dict[str, JobState] = {}


# ─── App Setup ───────────────────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: ensure folders exist
    for folder in [BASE_INPUT_FOLDER, BASE_PROMPT_FOLDER, OUTPUT_FOLDER]:
        os.makedirs(folder, exist_ok=True)
    yield
    # Shutdown: cleanup

app = FastAPI(title="Gemini Auto Tool API", lifespan=lifespan)

# CORS for React dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─── Request/Response Models ─────────────────────────────────────────────

class GenerateFrontRequest(BaseModel):
    product: str
    sku: str
    resolution: str = "1K"
    reference_image_path: Optional[str] = None
    match_pose: bool = False
    match_bg: bool = False

class GenerateVariantsRequest(BaseModel):
    product: str
    sku: str
    resolution: str = "1K"
    selected_poses: list[str]  # e.g. ["Back", "Side", "Neck", "Detail"]
    front_image_path: Optional[str] = None  # path to saved front image

class AutoTuneRequest(BaseModel):
    product: str

class CreateProductRequest(BaseModel):
    name: str
    category: str  # "top", "bottom", "dress"
    initial_color: str  # First SKU/color name

class SavePromptsRequest(BaseModel):
    master_prompt: Optional[str] = None
    variants: Optional[dict[str, str]] = None  # {"Back": "content", ...}


# ─── API Endpoints ───────────────────────────────────────────────────────

# --- Products ---

@app.get("/api/products")
def list_products():
    """List available products from input_images/ folder."""
    if not os.path.exists(BASE_INPUT_FOLDER):
        return {"products": []}
    products = [d for d in os.listdir(BASE_INPUT_FOLDER)
                if os.path.isdir(os.path.join(BASE_INPUT_FOLDER, d))]
    return {"products": products}


@app.post("/api/products")
def create_product(req: CreateProductRequest):
    """Create a new product with prompt templates and initial SKU folder."""
    product_name = req.name.strip()
    if not product_name:
        raise HTTPException(400, "Product name is required")
    
    prompt_dir = os.path.join(BASE_PROMPT_FOLDER, product_name)
    input_dir = os.path.join(BASE_INPUT_FOLDER, product_name, req.initial_color.strip())
    
    if os.path.exists(prompt_dir):
        raise HTTPException(409, f"Product '{product_name}' already exists")
    
    os.makedirs(prompt_dir, exist_ok=True)
    os.makedirs(input_dir, exist_ok=True)
    
    # Generate prompt templates based on category
    templates = _get_prompt_templates(product_name, req.category.lower())
    for filename, content in templates.items():
        filepath = os.path.join(prompt_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
    
    return {
        "status": "created",
        "product": product_name,
        "prompt_files": list(templates.keys()),
        "sku": req.initial_color.strip()
    }


@app.post("/api/products/{product_name}/skus")
def create_sku(product_name: str, color: str = Form(...)):
    """Add a new color/SKU folder for an existing product."""
    color_name = color.strip()
    if not color_name:
        raise HTTPException(400, "Color name is required")
    
    product_input_dir = os.path.join(BASE_INPUT_FOLDER, product_name)
    if not os.path.exists(product_input_dir):
        raise HTTPException(404, f"Product '{product_name}' not found")
    
    sku_dir = os.path.join(product_input_dir, color_name)
    if os.path.exists(sku_dir):
        raise HTTPException(409, f"Color '{color_name}' already exists")
    
    os.makedirs(sku_dir)
    return {"status": "created", "sku": color_name}


@app.post("/api/products/{product_name}/{sku_name}/upload")
async def upload_sku_image(
    product_name: str,
    sku_name: str,
    image_type: str = Form(...),  # Front, Back, Side, Detail, Neck, etc.
    file: UploadFile = File(...)
):
    """Upload an image for a SKU, automatically renamed by type."""
    sku_dir = os.path.join(BASE_INPUT_FOLDER, product_name, sku_name)
    if not os.path.exists(sku_dir):
        raise HTTPException(404, f"SKU folder not found: {product_name}/{sku_name}")
    
    ext = os.path.splitext(file.filename)[1] or ".jpg"
    safe_name = f"{image_type.strip()}{ext}"
    save_path = os.path.join(sku_dir, safe_name)
    
    content = await file.read()
    with open(save_path, "wb") as f:
        f.write(content)
    
    return {
        "status": "uploaded",
        "filename": safe_name,
        "path": save_path,
        "preview_url": f"/api/input-image/{product_name}/{sku_name}/{safe_name}"
    }


@app.post("/api/products/{product_name}/prompts")
def save_prompts(product_name: str, req: SavePromptsRequest):
    """Save edited prompt files for a product."""
    prompt_dir = os.path.join(BASE_PROMPT_FOLDER, product_name)
    if not os.path.exists(prompt_dir):
        raise HTTPException(404, f"Prompts not found for '{product_name}'")
    
    saved_files = []
    
    # Save master prompt
    if req.master_prompt is not None:
        master_path = os.path.join(prompt_dir, "master_prompt.txt")
        with open(master_path, "w", encoding="utf-8") as f:
            f.write(req.master_prompt)
        saved_files.append("master_prompt.txt")
    
    # Save variant prompts
    if req.variants:
        for variant_key, content in req.variants.items():
            # Convert key like "Back" -> "back.txt"
            filename = f"{variant_key.lower()}.txt"
            filepath = os.path.join(prompt_dir, filename)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            saved_files.append(filename)
    
    return {"status": "saved", "files": saved_files}


@app.delete("/api/products/{product_name}")
def delete_product(product_name: str):
    """Delete a product's prompt and input folders."""
    prompt_dir = os.path.join(BASE_PROMPT_FOLDER, product_name)
    input_dir = os.path.join(BASE_INPUT_FOLDER, product_name)
    
    deleted = []
    if os.path.exists(prompt_dir):
        shutil.rmtree(prompt_dir)
        deleted.append("prompts")
    if os.path.exists(input_dir):
        shutil.rmtree(input_dir)
        deleted.append("input_images")
    
    if not deleted:
        raise HTTPException(404, f"Product '{product_name}' not found")
    
    return {"status": "deleted", "product": product_name, "deleted": deleted}


@app.delete("/api/products/{product_name}/skus/{sku_name}")
def delete_sku(product_name: str, sku_name: str):
    """Delete a specific SKU/color folder."""
    sku_dir = os.path.join(BASE_INPUT_FOLDER, product_name, sku_name)
    if not os.path.exists(sku_dir):
        raise HTTPException(404, f"SKU '{sku_name}' not found")
    shutil.rmtree(sku_dir)
    return {"status": "deleted", "sku": sku_name}


@app.get("/api/products/{product_name}/skus")
def list_skus(product_name: str):
    """List SKU folders for a product."""
    product_path = os.path.join(BASE_INPUT_FOLDER, product_name)
    if not os.path.exists(product_path):
        raise HTTPException(404, f"Product '{product_name}' not found")
    
    skus = [d for d in os.listdir(product_path)
            if os.path.isdir(os.path.join(product_path, d))]
    return {"skus": skus, "total": len(skus)}


@app.get("/api/products/{product_name}/poses")
def list_poses(product_name: str):
    """Get available poses/variants for a product (from Prompts/ folder)."""
    prompt_path = os.path.join(BASE_PROMPT_FOLDER, product_name)
    if not os.path.exists(prompt_path):
        raise HTTPException(404, f"Prompts not found for '{product_name}'")
    
    extra_tasks = utils.get_extra_tasks(prompt_path)
    poses = ["Front"]  # Front is always available
    for task in extra_tasks:
        key = task["suffix"].replace("_", "")
        if key != "Front":
            poses.append(key)
    return {"poses": poses, "tasks": extra_tasks}


@app.get("/api/products/{product_name}/prompts")
def get_prompts(product_name: str):
    """Read master prompt + variant prompt contents."""
    prompt_path = os.path.join(BASE_PROMPT_FOLDER, product_name)
    master_path = os.path.join(prompt_path, "master_prompt.txt")
    
    master_prompt = utils.read_file(master_path)
    if not master_prompt:
        raise HTTPException(404, f"master_prompt.txt not found for '{product_name}'")
    
    # Read variant prompts
    variants = {}
    extra_tasks = utils.get_extra_tasks(prompt_path)
    for task in extra_tasks:
        key = task["suffix"].replace("_", "")
        content = utils.read_file(task["file"])
        if content:
            variants[key] = content
    
    return {"master_prompt": master_prompt, "variants": variants}


@app.get("/api/products/{product_name}/sku/{sku_name}/images")
def list_sku_images(product_name: str, sku_name: str):
    """List images in a specific SKU folder."""
    sku_path = os.path.join(BASE_INPUT_FOLDER, product_name, sku_name)
    if not os.path.exists(sku_path):
        raise HTTPException(404, f"SKU '{sku_name}' not found")
    
    valid_exts = ('.png', '.jpg', '.jpeg', '.heic', '.heif', '.webp')
    images = [f for f in os.listdir(sku_path) if f.lower().endswith(valid_exts)]
    
    return {
        "images": images,
        "paths": [f"/api/input-image/{product_name}/{sku_name}/{f}" for f in images]
    }


# --- Image Serving ---

@app.get("/api/input-image/{product_name}/{sku_name}/{filename}")
def serve_input_image(product_name: str, sku_name: str, filename: str):
    """Serve an input image file."""
    file_path = os.path.join(BASE_INPUT_FOLDER, product_name, sku_name, filename)
    if not os.path.exists(file_path):
        raise HTTPException(404, "Image not found")
    return FileResponse(file_path)


@app.get("/api/input-image/{product_name}/{filename}")
def serve_product_level_image(product_name: str, filename: str):
    """Serve a product-level image (reference images etc.)."""
    file_path = os.path.join(BASE_INPUT_FOLDER, product_name, filename)
    if not os.path.exists(file_path):
        raise HTTPException(404, "Image not found")
    return FileResponse(file_path)


@app.get("/api/output-image/{product_name}/{folder}/{filename}")
def serve_output_image(product_name: str, folder: str, filename: str):
    """Serve a generated output image."""
    file_path = os.path.join(OUTPUT_FOLDER, product_name, folder, filename)
    if not os.path.exists(file_path):
        raise HTTPException(404, "Image not found")
    return FileResponse(file_path)


# --- Reference Image Upload ---

@app.post("/api/upload/reference")
async def upload_reference_image(file: UploadFile = File(...)):
    """Upload a reference image, return the saved path."""
    upload_dir = os.path.join(BASE_INPUT_FOLDER, "_web_uploads")
    os.makedirs(upload_dir, exist_ok=True)
    
    # Save with unique name
    ext = os.path.splitext(file.filename)[1]
    saved_name = f"ref_{uuid.uuid4().hex[:8]}{ext}"
    saved_path = os.path.join(upload_dir, saved_name)
    
    content = await file.read()
    with open(saved_path, "wb") as f:
        f.write(content)
    
    return {"path": saved_path, "filename": saved_name}


# --- Reference Image Analysis ---

@app.post("/api/analyze-reference")
def analyze_reference(image_path: str = Form(...)):
    """Analyze a reference image using Gemini to extract pose/background."""
    if not os.path.exists(image_path):
        raise HTTPException(404, "Reference image not found")
    
    results = api_client.analyze_reference_image(image_path)
    if not results:
        raise HTTPException(500, "Reference analysis failed")
    
    return {"analysis": results}


# --- Generation ---

@app.post("/api/generate/start")
def start_generation(req: GenerateFrontRequest):
    """
    Start the full generation pipeline for a product:
    Generates front image for each SKU sequentially.
    Returns a job_id to track via SSE.
    """
    job_id = uuid.uuid4().hex[:12]
    job = JobState(job_id)
    active_jobs[job_id] = job
    
    # Start generation in background thread
    thread = threading.Thread(
        target=_run_front_generation,
        args=(job, req),
        daemon=True
    )
    thread.start()
    
    return {"job_id": job_id}


@app.post("/api/generate/save-and-variants")
def save_and_generate_variants(req: GenerateVariantsRequest):
    """
    Save the front image and generate all selected variants.
    Returns a job_id to track via SSE.
    """
    job_id = uuid.uuid4().hex[:12]
    job = JobState(job_id)
    active_jobs[job_id] = job
    
    thread = threading.Thread(
        target=_run_variant_generation,
        args=(job, req),
        daemon=True
    )
    thread.start()
    
    return {"job_id": job_id}


@app.post("/api/generate/save-front")
def save_front_only(
    product: str = Form(...),
    sku: str = Form(...),
    image_data: str = Form(...)  # base64 encoded image
):
    """Save the current front image to output folder. Returns the saved path."""
    product_output = os.path.join(OUTPUT_FOLDER, product)
    os.makedirs(product_output, exist_ok=True)
    
    sku_output = utils.get_unique_folder(product_output, sku)
    
    output_filename = f"{sku}_Front.jpg"
    saved_path = os.path.join(sku_output, output_filename)
    
    # Decode and save
    from PIL import Image
    image_bytes = base64.b64decode(image_data)
    img = Image.open(io.BytesIO(image_bytes))
    img.convert('RGB').save(saved_path, quality=100)
    
    return {
        "saved_path": saved_path,
        "output_folder": sku_output,
        "filename": output_filename
    }


@app.post("/api/generate/cancel/{job_id}")
def cancel_generation(job_id: str):
    """Cancel a running generation job."""
    job = active_jobs.get(job_id)
    if not job:
        raise HTTPException(404, "Job not found")
    
    job.cancel()
    return {"status": "cancelled"}


# --- SSE Event Stream ---

@app.get("/api/generate/stream/{job_id}")
async def stream_generation_events(job_id: str):
    """SSE endpoint to stream generation progress events."""
    job = active_jobs.get(job_id)
    if not job:
        raise HTTPException(404, "Job not found")
    
    async def event_generator():
        last_index = 0
        while True:
            # Check for new events
            with job.lock:
                new_events = job.events[last_index:]
                last_index = len(job.events)
            
            for event in new_events:
                yield f"data: {json.dumps(event)}\n\n"
                
                # If we got a 'done' or 'error' event, stop
                if event["type"] in ("done", "error", "cancelled"):
                    return
            
            if job.cancelled:
                yield f"data: {json.dumps({'type': 'cancelled', 'data': {}})}\n\n"
                return
            
            await asyncio.sleep(0.3)
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        }
    )


# --- Auto-Tune ---

@app.post("/api/auto-tune")
def auto_tune(req: AutoTuneRequest):
    """Run auto-tune on a product's prompts."""
    result = configure_prompts.auto_tune_prompts(req.product)
    if result == "Success":
        return {"status": "success", "message": "Prompts auto-tuned and reloaded"}
    else:
        raise HTTPException(500, f"Auto-tune failed: {result}")


# --- Download ---

@app.get("/api/download/{product_name}/{folder_name}")
def download_as_zip(product_name: str, folder_name: str):
    """Download all images in an output folder as a ZIP."""
    folder_path = os.path.join(OUTPUT_FOLDER, product_name, folder_name)
    if not os.path.exists(folder_path):
        raise HTTPException(404, "Output folder not found")
    
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
        for filename in os.listdir(folder_path):
            filepath = os.path.join(folder_path, filename)
            if os.path.isfile(filepath):
                zf.write(filepath, filename)
    
    zip_buffer.seek(0)
    return StreamingResponse(
        zip_buffer,
        media_type="application/zip",
        headers={"Content-Disposition": f"attachment; filename={folder_name}.zip"}
    )


# ─── Prompt Template Factory ──────────────────────────────────────────────

def _get_prompt_templates(product_name: str, category: str) -> dict[str, str]:
    """
    Generate default prompt template files based on product category.
    Returns a dict of {filename: content}.
    """
    name_lower = product_name.lower()
    
    # Mandatory rules baked into every prompt
    FIDELITY_RULE = (
        "STRICT REQUIREMENT: The generated product must match the Input Image (Raw Product) "
        "with 100% fidelity. DO NOT alter the color, fabric texture, or stitching details.\n"
        "STRICT PROHIBITION: CHANGING COLOR IS NOT ALLOWED. The generated product MUST have "
        "the EXACT SAME COLOR as the Input Image. Do not lighten, darken, or shift the hue."
    )
    WRINKLE_RULE = (
        "STRICT REQUIREMENT: THE PRODUCT MUST BE TOTALLY WRINKLE-FREE. REMOVE ALL CREASES, "
        "FOLDS, AND WRINKLES. The fabric must appear perfectly smooth and professionally ironed. "
        "Even if the Input Image shows wrinkles, you MUST fix them."
    )
    HALLUCINATION_RULE = (
        "STRICT PROHIBITION: NO NEW PATTERNS. Do not generate any stitching, ribbing, or designs "
        "that are not in the Input Image. If the input is solid/plain, the output MUST be solid/plain."
    )
    
    MANDATORY_BLOCK = f"\n\n{FIDELITY_RULE}\n\n{WRINKLE_RULE}\n\n{HALLUCINATION_RULE}"
    
    # Category-specific structures
    if category == "bottom":
        templates = {
            "master_prompt.txt": f"""Generate a photorealistic e-commerce image of a model wearing the {name_lower}.

Input References:
- Image 1 (Raw Product): The ONLY source for the {name_lower} structure, fabric, and color.
- Image 2 (Style Reference): Source for Layout, Background, Props, and Lighting.

Instructions:
1. Product Accuracy: The {name_lower} must be IDENTICAL to Image 1.
2. Layout & Style: Follow Image 2's background and lighting.
3. Complementary Styling: Pair with a crisp white t-shirt tucked in and white minimalist sneakers.

Negative prompt: no pattern alteration, no color change, wrinkles, creases, no logo, no added textures{MANDATORY_BLOCK}""",

            "back.txt": f"""Generate a high-resolution image of the model from behind, showcasing the back of the {name_lower}.

Input References:
- Image 1 (Generated Front): Source for BACKGROUND, LIGHTING, STYLE, and MODEL.
- Image 2 (Raw Product Image): Source for REAL LIFE PRODUCT DETAILS from the back.

Instructions:
1. Background & Lighting: STRICTLY MATCH Image 1.
2. Product: Use Image 2 for back details (pockets, yoke, seams). Color and texture must match Image 1.
3. Model: Same model, same outfit (white t-shirt, white sneakers), same skin tone as Image 1.

Negative prompt: no mismatched background, no color change, nail polish{MANDATORY_BLOCK}""",

            "waistband.txt": f"""Generate a high-resolution close-up detail shot of the WAISTBAND area of the {name_lower}.

Input References:
- Image 1 (Generated Front): Source for BACKGROUND, LIGHTING, STYLE.
- Image 2 (Raw Product Image): Source for REAL LIFE waistband construction details.

Instructions:
1. Background & Lighting: STRICTLY MATCH Image 1.
2. Product: Show button, zipper fly, belt loops, and waistband stitching exactly as in Image 2.
3. Color and texture must match Image 1.

Negative prompt: no full body view, no mismatched background{MANDATORY_BLOCK}""",

            "detail.txt": f"""Generate a high-resolution MACRO DETAIL shot of the fabric/texture of the {name_lower}.

Input References:
- Image 1 (Generated Front): Source for BACKGROUND, LIGHTING.
- Image 2 (Raw Product Image): Source for REAL LIFE fabric texture (weave, print quality).

Instructions:
1. Background & Lighting: STRICTLY MATCH Image 1's mood.
2. Product: Extreme close-up of fabric. Color and texture must match Image 1.

Negative prompt: no full view, no conflicting patterns{MANDATORY_BLOCK}""",

            "side.txt": f"""Generate a high-resolution image of the model from the side, showcasing the side profile of the {name_lower}.

Input References:
- Image 1 (Generated Front): Source for BACKGROUND, LIGHTING, STYLE, and MODEL.
- Image 2 (Raw Product Image): Source for side profile details.

Instructions:
1. Background & Lighting: STRICTLY MATCH Image 1.
2. Product: Side profile showing fit and drape. Color and texture must match Image 1.
3. Model: Same model, same outfit (white t-shirt, white sneakers), same skin tone.

Negative prompt: no mismatched background, nail polish{MANDATORY_BLOCK}""",
        }
    elif category == "top":
        templates = {
            "master_prompt.txt": f"""Generate a photorealistic e-commerce image of a model wearing the {name_lower}.

Input References:
- Image 1 (Raw Product): The ONLY source for the {name_lower} structure, fabric, and color.
- Image 2 (Style Reference): Source for Layout, Background, Props, and Lighting.

Instructions:
1. Product Accuracy: The {name_lower} must be IDENTICAL to Image 1.
2. Layout & Style: Follow Image 2's background and lighting.
3. Complementary Styling: Pair with light wash denim jeans and white minimalist sneakers.

Negative prompt: no pattern alteration, no color change, wrinkles, creases, no logo, no added textures{MANDATORY_BLOCK}""",

            "back.txt": f"""Generate a high-resolution image of the model from behind, showcasing the back of the {name_lower}.

Input References:
- Image 1 (Generated Front): Source for BACKGROUND, LIGHTING, STYLE, and MODEL.
- Image 2 (Raw Product Image): Source for REAL LIFE PRODUCT DETAILS.

Instructions:
1. Background & Lighting: STRICTLY MATCH Image 1.
2. Product: Back view details from Image 2. Color and texture must match Image 1.
3. Model: Same model, same outfit (denim jeans, white sneakers), same skin tone.

Negative prompt: no mismatched background, nail polish{MANDATORY_BLOCK}""",

            "neck.txt": f"""Generate a high-resolution close-up Detail Shot of the NECKLINE/COLLAR area of the {name_lower}.

Input References:
- Image 1 (Generated Front): Source for BACKGROUND, LIGHTING, STYLE.
- Image 2 (Raw Product Image): Source for REAL LIFE collar/neckline construction.

Instructions:
1. Background & Lighting: STRICTLY MATCH Image 1.
2. Product: Show collar, stitching, buttons exactly as in Image 2.

Negative prompt: no full body view, no fuzzy details{MANDATORY_BLOCK}""",

            "detail.txt": f"""Generate a high-resolution MACRO DETAIL shot of the fabric/texture of the {name_lower}.

Input References:
- Image 1 (Generated Front): Source for BACKGROUND, LIGHTING.
- Image 2 (Raw Product Image): Source for REAL LIFE fabric texture.

Instructions:
1. Extreme close-up (Macro) view of the fabric.
2. Color and texture must match Image 1.

Negative prompt: no full view, no conflicting patterns{MANDATORY_BLOCK}""",

            "side.txt": f"""Generate a high-resolution image of the model from the side, showcasing the {name_lower}.

Input References:
- Image 1 (Generated Front): Source for BACKGROUND, LIGHTING, STYLE, and MODEL.
- Image 2 (Raw Product Image): Source for side profile details.

Instructions:
1. Background & Lighting: STRICTLY MATCH Image 1.
2. Model: Same model, same outfit (denim jeans, white sneakers), same skin tone.

Negative prompt: no mismatched background, nail polish{MANDATORY_BLOCK}""",
        }
    else:  # dress or default
        templates = {
            "master_prompt.txt": f"""Generate a photorealistic e-commerce image of a model wearing the {name_lower}.

Input References:
- Image 1 (Raw Product): The ONLY source for the {name_lower} structure, fabric, and color.
- Image 2 (Style Reference): Source for Layout, Background, Props, and Lighting.

Instructions:
1. Product Accuracy: The {name_lower} must be IDENTICAL to Image 1.
2. Layout & Style: Follow Image 2's background and lighting.
3. Complementary Styling: Pair with elegant heels or minimalist sandals.

Negative prompt: no pattern alteration, no color change, wrinkles, creases, no logo, no added textures{MANDATORY_BLOCK}""",

            "back.txt": f"""Generate a high-resolution image of the model from behind, showcasing the back of the {name_lower}.

Input References:
- Image 1 (Generated Front): Source for BACKGROUND, LIGHTING, STYLE, and MODEL.
- Image 2 (Raw Product Image): Source for REAL LIFE back details.

Instructions:
1. Background & Lighting: STRICTLY MATCH Image 1.
2. Product: Back view from Image 2. Color and texture must match Image 1.
3. Model: Same model, same accessories, same skin tone.

Negative prompt: no mismatched background, nail polish{MANDATORY_BLOCK}""",

            "neck.txt": f"""Generate a high-resolution close-up Detail Shot of the NECKLINE area of the {name_lower}.

Input References:
- Image 1 (Generated Front): Source for BACKGROUND, LIGHTING.
- Image 2 (Raw Product Image): Source for neckline construction details.

Instructions:
1. Close-up of neckline. Match background and lighting from Image 1.

Negative prompt: no full body view{MANDATORY_BLOCK}""",

            "detail.txt": f"""Generate a high-resolution MACRO DETAIL shot of the fabric/texture of the {name_lower}.

Input References:
- Image 1 (Generated Front): Source for BACKGROUND, LIGHTING.
- Image 2 (Raw Product Image): Source for fabric texture.

Instructions:
1. Extreme close-up of fabric. Color and texture must match Image 1.

Negative prompt: no full view, no conflicting patterns{MANDATORY_BLOCK}""",

            "side.txt": f"""Generate a high-resolution image of the model from the side, showcasing the {name_lower}.

Input References:
- Image 1 (Generated Front): Source for BACKGROUND, LIGHTING, STYLE, and MODEL.
- Image 2 (Raw Product Image): Source for side details and hem drape.

Instructions:
1. Background & Lighting: STRICTLY MATCH Image 1.
2. Model: Same model, same accessories, same skin tone.

Negative prompt: no mismatched background, nail polish{MANDATORY_BLOCK}""",
        }
    
    return templates


# ─── Background Generation Logic ─────────────────────────────────────────

def _get_sku_images(product_name: str, sku_name: str):
    """Get all valid images in a SKU folder + product-level reference."""
    sku_path = os.path.join(BASE_INPUT_FOLDER, product_name, sku_name)
    valid_exts = ('.png', '.jpg', '.jpeg', '.heic', '.heif')
    
    sku_images = []
    if os.path.exists(sku_path):
        sku_images = [os.path.join(sku_path, f) for f in os.listdir(sku_path)
                      if f.lower().endswith(valid_exts)]
    
    # Find product-level reference image
    product_path = os.path.join(BASE_INPUT_FOLDER, product_name)
    product_level_files = [
        os.path.join(product_path, f)
        for f in os.listdir(product_path)
        if os.path.isfile(os.path.join(product_path, f)) and f.lower().endswith(valid_exts)
    ]
    
    ref_image = None
    if product_level_files:
        ref_image = next((f for f in product_level_files if "reference" in os.path.basename(f).lower()), None)
        if not ref_image:
            ref_image = product_level_files[0]
    
    return sku_images, ref_image


def _run_front_generation(job: JobState, req: GenerateFrontRequest):
    """Generate the front image for a specific SKU. Runs in background thread."""
    try:
        job.push_event("status", {"message": f"Preparing front generation for {req.sku}..."})
        
        # Get images
        sku_images, product_ref = _get_sku_images(req.product, req.sku)
        
        # Find front image
        front_img = next((img for img in sku_images if "front" in os.path.basename(img).lower()), None)
        if not front_img and sku_images:
            front_img = sku_images[0]
        
        input_images = []
        if front_img:
            input_images.append(front_img)
        if product_ref:
            input_images.append(product_ref)
        
        if not input_images:
            job.push_event("error", {"message": f"No images found for SKU: {req.sku}"})
            return
        
        # Load master prompt
        master_prompt_path = os.path.join(BASE_PROMPT_FOLDER, req.product, "master_prompt.txt")
        prompt = utils.read_file(master_prompt_path)
        if not prompt:
            job.push_event("error", {"message": f"Master prompt not found for {req.product}"})
            return
        
        # Handle reference image analysis
        if req.reference_image_path and os.path.exists(req.reference_image_path):
            if req.match_pose or req.match_bg:
                job.push_event("status", {"message": "Analyzing reference image..."})
                analysis = api_client.analyze_reference_image(req.reference_image_path)
                if analysis:
                    prompt = api_client.inject_prompt_overrides(
                        prompt, analysis,
                        inject_pose=req.match_pose,
                        inject_bg=req.match_bg
                    )
        
        # Generate with retry (mirrors main.py retry logic)
        job.push_event("status", {"message": f"Generating front view for {req.sku}..."})
        
        attempt = 0
        while not job.cancelled:
            attempt += 1
            result_img, error_msg = api_client.fetch_image_from_api(
                prompt, input_images,
                aspect_ratio="1:1",
                image_size=req.resolution
            )
            
            if result_img:
                # Convert to base64 for sending to frontend
                buf = io.BytesIO()
                result_img.convert('RGB').save(buf, format='JPEG', quality=100)
                b64 = base64.b64encode(buf.getvalue()).decode('utf-8')
                
                # Also provide the raw input paths for variant generation
                job.push_event("front_ready", {
                    "image_base64": b64,
                    "sku": req.sku,
                    "input_images": [os.path.basename(p) for p in sku_images],
                    "all_sku_images": sku_images,
                })
                job.push_event("done", {"message": "Front generation complete"})
                return
            
            job.push_event("status", {
                "message": f"Generation failed ({error_msg}). Retrying (attempt {attempt})..."
            })
            time.sleep(1)
        
        job.push_event("cancelled", {})
    
    except Exception as e:
        job.push_event("error", {"message": str(e)})


def _run_variant_generation(job: JobState, req: GenerateVariantsRequest):
    """Generate variant images (Back, Side, Neck, Detail, etc.). Runs in background thread."""
    try:
        product_path = os.path.join(BASE_PROMPT_FOLDER, req.product)
        extra_tasks = utils.get_extra_tasks(product_path)
        
        # Get SKU raw images for smart matching
        sku_images, _ = _get_sku_images(req.product, req.sku)
        sku_path = os.path.join(BASE_INPUT_FOLDER, req.product, req.sku)
        
        # Identify specific raw images by keyword (mirrors main.py logic)
        raw_back = next((p for p in sku_images if "back" in os.path.basename(p).lower()), None)
        raw_front = next((p for p in sku_images if "front" in os.path.basename(p).lower()), None)
        raw_neck = next((p for p in sku_images if "neck" in os.path.basename(p).lower()), None)
        raw_detail = next((p for p in sku_images if "detail" in os.path.basename(p).lower()), None)
        raw_side = next((p for p in sku_images if "side" in os.path.basename(p).lower()), None)
        fallback_raw = sku_images[0] if sku_images else None
        
        # Prepare output folder
        product_output = os.path.join(OUTPUT_FOLDER, req.product)
        os.makedirs(product_output, exist_ok=True)
        
        # Check if front image already saved, otherwise create output folder
        output_folder = None
        if req.front_image_path and os.path.exists(req.front_image_path):
            output_folder = os.path.dirname(req.front_image_path)
        else:
            output_folder = utils.get_unique_folder(product_output, req.sku)
        
        # Filter tasks to only selected poses
        selected_tasks = []
        for task in extra_tasks:
            pose_key = task["suffix"].replace("_", "")
            if pose_key in req.selected_poses:
                selected_tasks.append(task)
        
        total = len(selected_tasks)
        results = []
        
        for i, task in enumerate(selected_tasks):
            if job.cancelled:
                job.push_event("cancelled", {})
                return
            
            pose_key = task["suffix"].replace("_", "")
            job.push_event("variant_progress", {
                "message": f"Generating {pose_key.upper()} ({i+1}/{total})...",
                "current": i + 1,
                "total": total,
                "pose": pose_key
            })
            
            prompt_text = utils.read_file(task["file"])
            if not prompt_text:
                continue
            
            # Build input list: [Generated Front] + [Specific Raw Image]
            current_inputs = []
            if req.front_image_path and os.path.exists(req.front_image_path):
                current_inputs.append(req.front_image_path)
            
            # Smart raw image matching (mirrors main.py logic)
            suffix = task["suffix"]
            chosen_raw = None
            if suffix == "_Back":
                chosen_raw = raw_back or raw_front or fallback_raw
            elif suffix == "_Neck":
                chosen_raw = raw_neck or raw_front or fallback_raw
            elif suffix == "_Detail":
                chosen_raw = raw_detail or raw_front or fallback_raw
            elif suffix == "_Side":
                chosen_raw = raw_side or raw_front or fallback_raw
            else:
                chosen_raw = raw_front or fallback_raw
            
            if chosen_raw:
                current_inputs.append(chosen_raw)
            
            # Generate with retry
            attempt = 0
            while not job.cancelled:
                attempt += 1
                result_img, error_msg = api_client.fetch_image_from_api(
                    prompt_text, current_inputs,
                    aspect_ratio=task["ratio"],
                    image_size=req.resolution
                )
                
                if result_img:
                    # Save variant
                    variant_filename = f"{req.sku}{task['suffix']}.jpg"
                    save_path = os.path.join(output_folder, variant_filename)
                    result_img.convert('RGB').save(save_path, quality=100)
                    
                    # Send to frontend
                    buf = io.BytesIO()
                    result_img.convert('RGB').save(buf, format='JPEG', quality=100)
                    b64 = base64.b64encode(buf.getvalue()).decode('utf-8')
                    
                    results.append({
                        "pose": pose_key,
                        "filename": variant_filename,
                        "path": save_path,
                        "image_base64": b64
                    })
                    
                    job.push_event("variant_ready", {
                        "pose": pose_key,
                        "filename": variant_filename,
                        "image_base64": b64,
                        "current": i + 1,
                        "total": total
                    })
                    break
                
                job.push_event("variant_progress", {
                    "message": f"Retrying {pose_key.upper()} (attempt {attempt})...",
                    "current": i + 1,
                    "total": total,
                    "pose": pose_key
                })
                time.sleep(1)
        
        if not job.cancelled:
            job.push_event("done", {
                "message": f"All {total} variants generated",
                "output_folder": output_folder,
                "results": [{k: v for k, v in r.items() if k != "image_base64"} for r in results]
            })
    
    except Exception as e:
        job.push_event("error", {"message": str(e)})


# ─── Entry Point ──────────────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
