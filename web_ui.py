
import streamlit as st
import os
import time
import shutil
import uuid
from PIL import Image

# Import existing modules
# We assume these are in the same directory
import config
from config import BASE_INPUT_FOLDER, BASE_PROMPT_FOLDER, OUTPUT_FOLDER, API_KEY, CHROME_PROFILE, CHROME_URL
import utils
import api_client
import configure_prompts

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Gemini 5-Shot Pipeline",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS STYLING ---
st.markdown("""
    <style>
    .block-container {
        padding-top: 1rem;
        padding-bottom: 5rem;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        font-weight: bold;
    }
    .status-box {
        padding: 10px;
        border-radius: 5px;
        background-color: #f0f2f6;
        border: 1px solid #d6d6d6;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# --- SESSION STATE INITIALIZATION ---
def init_session_state():
    defaults = {
        "current_product": None,
        "sku_folders": [],
        "current_index": 0,
        "input_folder": None,
        "extra_tasks": [],
        "master_prompt": "",
        "current_batch_prompt": "",
        
        "current_generated_image": None, 
        "current_image_path": None, # If saved
        "is_processing": False,
        
        # Pending Batch State (equivalent to self.pending_batch_args)
        # Stores: (raw_paths, saved_front_path, base_name, output_folder)
        "pending_batch_data": None,
        
        # UI State
        "status_message": "Ready. Select a product to begin.",
        "batch_logs": [],
        "error_msg": None,
        
        # Checkbox defaults handled by st.checkbox key persistence
    }
    
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

init_session_state()

# --- HELPER FUNCTIONS ---

def get_available_products():
    if not os.path.exists(BASE_INPUT_FOLDER):
        os.makedirs(BASE_INPUT_FOLDER)
        return []
    return [d for d in os.listdir(BASE_INPUT_FOLDER) if os.path.isdir(os.path.join(BASE_INPUT_FOLDER, d))]

def load_product_context(product_name):
    """Refreshes the state when product changes."""
    st.session_state.current_product = product_name
    
    # Paths
    input_folder = os.path.join(BASE_INPUT_FOLDER, product_name)
    st.session_state.input_folder = input_folder
    prompt_path = os.path.join(BASE_PROMPT_FOLDER, product_name)
    
    # Ensure exists
    if not os.path.exists(input_folder):
        os.makedirs(input_folder)
    
    # Load Master Prompt
    master_file = os.path.join(prompt_path, "master_prompt.txt")
    st.session_state.master_prompt = utils.read_file(master_file) or ""
    st.session_state.current_batch_prompt = st.session_state.master_prompt
    
    # Load Extra Tasks (Variants)
    st.session_state.extra_tasks = utils.get_extra_tasks(prompt_path)
    
    # Load SKU Folders
    if os.path.exists(input_folder):
        items = os.listdir(input_folder)
        st.session_state.sku_folders = [d for d in items if os.path.isdir(os.path.join(input_folder, d))]
    else:
        st.session_state.sku_folders = []
    
    # Reset Per-Product State
    st.session_state.current_index = 0
    st.session_state.current_generated_image = None
    st.session_state.pending_batch_data = None
    st.session_state.batch_logs = []
    st.session_state.status_message = f"Loaded {product_name}. Total SKUs: {len(st.session_state.sku_folders)}"

def get_current_sku_name():
    if 0 <= st.session_state.current_index < len(st.session_state.sku_folders):
        return st.session_state.sku_folders[st.session_state.current_index]
    return None

# --- CORE LOGIC IMPLEMENTATION (Matching main.py) ---

def run_front_generation(resolution, ref_image_path, use_pose, use_bg, pose_enabled):
    sku_name = get_current_sku_name()
    if not sku_name:
        st.error("No SKU selected or available.")
        return

    st.session_state.status_message = f"Generating Front View for {sku_name}..."
    st.session_state.batch_logs = []
    
    # 1. Inputs Preparation
    sku_path = os.path.join(st.session_state.input_folder, sku_name)
    valid_exts = ('.png', '.jpg', '.jpeg', '.heic', '.heif')
    sku_images_all = [os.path.join(sku_path, f) for f in os.listdir(sku_path) if f.lower().endswith(valid_exts)]
    
    if not sku_images_all:
        st.error(f"No images found in {sku_name}")
        return

    # Find Front
    front_img = next((img for img in sku_images_all if "front" in os.path.basename(img).lower()), None)
    if not front_img: front_img = sku_images_all[0]
    
    current_sku_images = [front_img]
    
    # Find Global Reference
    product_level_files = [
        os.path.join(st.session_state.input_folder, f) 
        for f in os.listdir(st.session_state.input_folder) 
        if os.path.isfile(os.path.join(st.session_state.input_folder, f)) and f.lower().endswith(valid_exts)
    ]
    if product_level_files:
        ref_image = next((f for f in product_level_files if "reference" in os.path.basename(f).lower()), None)
        if not ref_image: ref_image = product_level_files[0]
        current_sku_images.append(ref_image)

    # 2. Ref Image Analysis Injection (Simulated loop from main.py logic)
    # The user might have run analysis via "Start" which updates prompts? 
    # In main.py `start_batch_action` calls analysis once before loop. 
    # We will do prompt updates here if ref_image_path is provided in UI.
    
    final_prompt = st.session_state.master_prompt
    
    if ref_image_path and os.path.exists(ref_image_path) and (use_pose or use_bg):
        with st.spinner("Analyzing Reference Image for overrides..."):
            analysis_results = api_client.analyze_reference_image(ref_image_path)
            if analysis_results:
                final_prompt = api_client.inject_prompt_overrides(
                    st.session_state.master_prompt,
                    analysis_results,
                    inject_pose=use_pose,
                    inject_bg=use_bg
                )
                st.session_state.current_batch_prompt = final_prompt # Persistence
                st.success("Reference overrides applied.")
    
    # 3. Generation Loop
    if pose_enabled: # "Front" checkbox
        generated_pil_image = None
        error_msg = None
        
        # Retry loop (simple version: 3 attempts)
        for attempt in range(3):
            with st.spinner(f"Generating Front View (Attempt {attempt+1}/3)..."):
                generated_pil_image, error_msg = api_client.fetch_image_from_api(
                    final_prompt, 
                    current_sku_images, 
                    aspect_ratio="1:1", 
                    image_size=resolution
                )
                if generated_pil_image:
                    break
                time.sleep(1)
        
        if generated_pil_image:
            st.session_state.current_generated_image = generated_pil_image
            st.session_state.status_message = "Front View Generated. Ready to Save."
            st.session_state.pending_batch_data = None # Reset
            st.rerun() # Refresh to show image
        else:
            st.error(f"Generation Failed: {error_msg}")
            st.session_state.error_msg = error_msg
    else:
        st.warning("Front View Skipped (Checkbox unchecked).")
        st.session_state.current_generated_image = None
        st.session_state.pending_batch_data = None
        st.rerun()

def save_front_logic():
    """Saves the current front image and updates pending_batch_data."""
    if not st.session_state.current_generated_image:
        return None
        
    sku_name = get_current_sku_name()
    product_output_folder = os.path.join(OUTPUT_FOLDER, st.session_state.current_product)
    
    sku_output_folder = utils.get_unique_folder(product_output_folder, sku_name)
    base_name = sku_name
    output_filename = f"{base_name}_Front.jpg"
    saved_path = os.path.join(sku_output_folder, output_filename)
    
    try:
        st.session_state.current_generated_image.convert('RGB').save(saved_path, quality=100)
        st.success(f"Saved Front: {saved_path}")
        
        # Prepare data for batch variants
        # Get raw images again 
        sku_path = os.path.join(st.session_state.input_folder, sku_name)
        valid_exts = ('.png', '.jpg', '.jpeg', '.heic', '.heif')
        sku_images_all = [os.path.join(sku_path, f) for f in os.listdir(sku_path) if f.lower().endswith(valid_exts)]
        
        return (sku_images_all, saved_path, base_name, sku_output_folder)
        
    except Exception as e:
        st.error(f"Save Error: {e}")
        return None

def run_batch_variants(batch_data, resolution, checked_variants):
    raw_paths, front_path, base_name, output_folder = batch_data
    
    # Identify specific Raws
    raw_back = next((p for p in raw_paths if "back" in os.path.basename(p).lower()), None)
    raw_front = next((p for p in raw_paths if "front" in os.path.basename(p).lower()), None)
    raw_neck = next((p for p in raw_paths if "neck" in os.path.basename(p).lower()), None)
    raw_detail = next((p for p in raw_paths if "detail" in os.path.basename(p).lower()), None)
    raw_side = next((p for p in raw_paths if "side" in os.path.basename(p).lower()), None)
    fallback = raw_paths[0] if raw_paths else None
    
    total = len(st.session_state.extra_tasks)
    progress_bar = st.progress(0)
    
    for i, task in enumerate(st.session_state.extra_tasks):
        pose_key = task["suffix"].replace("_", "")
        
        # Check against UI checkboxes
        if pose_key not in checked_variants or not checked_variants[pose_key]:
            progress_bar.progress((i + 1) / total)
            continue
            
        prompt_text = utils.read_file(task["file"])
        if not prompt_text: continue
        
        # Inputs: [Generated Front] + [Specific Raw]
        current_inputs = [front_path] if front_path else []
        
        suffix = task["suffix"]
        chosen_raw = None
        
        if suffix == "_Back": chosen_raw = raw_back or raw_front or fallback
        elif suffix == "_Neck": chosen_raw = raw_neck or raw_front or fallback
        elif suffix == "_Detail": chosen_raw = raw_detail or raw_front or fallback
        elif suffix == "_Side": chosen_raw = raw_side or raw_front or fallback
        else: chosen_raw = raw_front or fallback
        
        if chosen_raw: current_inputs.append(chosen_raw)
        
        st.session_state.batch_logs.append(f"Generating {pose_key}...")
        
        # Generate with Retry
        result_img = None
        for attempt in range(3):
            # Update logs in place? No, just spinner
            result_img, err = api_client.fetch_image_from_api(
                prompt_text, current_inputs, 
                aspect_ratio=task["ratio"], 
                image_size=resolution
            )
            if result_img: break
            time.sleep(1)
            
        if result_img:
            save_path = os.path.join(output_folder, f"{base_name}{suffix}.jpg")
            result_img.convert('RGB').save(save_path, quality=100)
            st.session_state.batch_logs.append(f"✅ Saved {pose_key}")
            # Optional: Show preview of variant? Maybe not to avoid clutter
        else:
             st.session_state.batch_logs.append(f"❌ Failed {pose_key}")
        
        progress_bar.progress((i + 1) / total)

    st.session_state.status_message = "Batch Complete."
    st.session_state.batch_logs.append("Done.")
    
    # Auto Advance
    st.session_state.current_index += 1
    st.session_state.current_generated_image = None
    st.session_state.pending_batch_data = None
    
    st.rerun()

# --- UI LAYOUT ---

# SIDEBAR
with st.sidebar:
    st.title("Settings")
    
    products = get_available_products()
    if not products:
        st.warning(f"No product folders found in {BASE_INPUT_FOLDER}")
        st.stop()
        
    # Product Select
    initial_idx = 0
    if st.session_state.current_product in products:
        initial_idx = products.index(st.session_state.current_product)
        
    selected_prod = st.selectbox("Product", products, index=initial_idx)
    
    # Context Trigger
    if selected_prod != st.session_state.current_product:
        load_product_context(selected_prod)
        st.rerun()

    # Resolution
    resolution = st.selectbox("Resolution", ["1K", "2K", "4K"], index=0)
    
    st.divider()
    
    # Poses
    st.subheader("Poses")
    
    # Control vars
    pose_checkboxes = {}
    
    col_cb1, col_cb2 = st.columns(2)
    with col_cb1:
        pose_checkboxes["Front"] = st.checkbox("Front", value=True)
    
    # Dynamic Poses
    for i, task in enumerate(st.session_state.extra_tasks):
        key = task["suffix"].replace("_", "")
        if key == "Front": continue
        # Default unchecked
        with (col_cb2 if i % 2 == 0 else col_cb1):
            pose_checkboxes[key] = st.checkbox(key, value=False)
    
    st.divider()
    
    # Reference Configuration
    st.subheader("Reference Image Override")
    ref_file_path = st.text_input("Ref Image Path (Optional)", help="Full path to a reference image to override style.")
    c1, c2 = st.columns(2)
    match_pose = c1.checkbox("Match Pose")
    match_bg = c2.checkbox("Match Background")
    
    auto_open_chrome = st.checkbox("Open Chrome on Save", value=False, help="Automatically open Chrome/Desktop when saving Front.")

    st.divider()
    
    # Auto-Tune
    if st.button("✨ Auto-Tune Prompts"):
        if st.session_state.current_product:
            with st.spinner(f"Auto-Tuning {st.session_state.current_product}..."):
                res = configure_prompts.auto_tune_prompts(st.session_state.current_product)
                if res == "Success":
                    load_product_context(st.session_state.current_product) # Reload
                    st.success("Prompts Updated!")
                else:
                    st.error(f"Failed: {res}")

# MAIN AREA
st.title(f"Gemini Pipeline: {st.session_state.current_product}")

# Status Bar
st.info(f"Status: {st.session_state.status_message}")

# Index Info
curr_sku = get_current_sku_name()
total_skus = len(st.session_state.sku_folders)
if not curr_sku:
    st.warning("No SKUs available.")
    st.stop()

st.markdown(f"#### SKU ({st.session_state.current_index + 1}/{total_skus}): **{curr_sku}**")

# Columnar Layout for Actions and Image
col_img, col_actions = st.columns([2, 1])

with col_img:
    img_container = st.empty()
    if st.session_state.current_generated_image:
        st.image(st.session_state.current_generated_image, caption=f"Generated Front: {curr_sku}")
    else:
        st.markdown(
            f"""<div style="background:#eee;height:400px;display:flex;align-items:center;justify-content:center;border-radius:10px;">
                <p style="color:#666;">No image generated yet.</p>
            </div>""", unsafe_allow_html=True
        )

with col_actions:
    st.subheader("Actions")
    
    # START BUTTON
    if st.button("▶ Start / Regenerate", type="primary"):
        run_front_generation(resolution, ref_file_path, match_pose, match_bg, pose_checkboxes.get("Front", True))

    st.divider()
    
    # SAVE & VARIANTS Logic
    # We have two states: Front Generated (Pending Save) -> Saved (Pending Variants)
    
    has_image = st.session_state.current_generated_image is not None
    is_saved = st.session_state.pending_batch_data is not None
    
    # Button: Save & Next (Generate Variants)
    # This button handles the full flow or the second half of the flow
    
    btn_label = "💾 Save Front"
    if is_saved:
        btn_label = "▶ Generate Variants"
    
    if st.button(btn_label, disabled=not has_image):
        if not is_saved:
            # Action: Save Front
            saved_data = save_front_logic()
            if saved_data:
                st.session_state.pending_batch_data = saved_data
                st.session_state.status_message = "Front Saved. Ready for variants."
                
                # Auto Desktop Trigger
                if auto_open_chrome:
                    try:
                        utils.create_desktop_and_open_chrome(CHROME_PROFILE, CHROME_URL, st.session_state.current_product)
                        st.session_state.batch_logs.append("Launched Chrome Automation.")
                    except Exception as e:
                        st.error(f"Auto-Desktop failed: {e}")
                
                st.rerun()
        else:
            # Action: Generate Variants & Next
            run_batch_variants(st.session_state.pending_batch_data, resolution, pose_checkboxes)

    # SKIP BUTTON
    if st.button("⏭ Skip"):
        st.session_state.current_index += 1
        st.session_state.current_generated_image = None
        st.session_state.pending_batch_data = None
        st.session_state.status_message = "Skipped."
        st.rerun()

    # Batch Logs (for variants)
    if st.session_state.batch_logs:
        st.markdown("**Batch Log:**")
        for log in st.session_state.batch_logs:
            st.text(log)

