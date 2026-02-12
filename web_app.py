"""
Gemini Auto Tool - Web Interface (Streamlit)
A simplified, user-friendly web app for generating product images.
"""

import os
import io
import uuid
import streamlit as st
from PIL import Image

# Import existing modules
from config import BASE_INPUT_FOLDER, BASE_PROMPT_FOLDER, OUTPUT_FOLDER, API_KEY
import utils
import api_client

# --- Page Configuration ---
st.set_page_config(
    page_title="Gemini Auto Tool",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for Modern Look ---
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f3460 0%, #1a1a2e 100%);
    }
    
    /* Headers */
    h1 {
        background: linear-gradient(90deg, #e94560, #ffa500);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #e94560, #ff6b6b);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(233, 69, 96, 0.3);
    }
    
    /* Cards/Containers */
    .css-1r6slb0 {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 1rem;
        backdrop-filter: blur(10px);
    }
    
    /* File uploader */
    [data-testid="stFileUploader"] {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 1rem;
    }
    
    /* Success messages */
    .stSuccess {
        background: rgba(0, 200, 100, 0.1);
        border-radius: 10px;
    }
    
    /* Progress bar */
    .stProgress > div > div {
        background: linear-gradient(90deg, #e94560, #ffa500);
    }
</style>
""", unsafe_allow_html=True)

# --- Session State Initialization ---
if 'session_id' not in st.session_state:
    st.session_state.session_id = uuid.uuid4().hex[:8]
if 'generated_images' not in st.session_state:
    st.session_state.generated_images = []
if 'current_front_image' not in st.session_state:
    st.session_state.current_front_image = None
if 'processing' not in st.session_state:
    st.session_state.processing = False

# --- Helper Functions ---
def get_available_products():
    """Get list of products from Prompts folder."""
    if not os.path.exists(BASE_PROMPT_FOLDER):
        return []
    return [d for d in os.listdir(BASE_PROMPT_FOLDER) 
            if os.path.isdir(os.path.join(BASE_PROMPT_FOLDER, d))]

def save_uploaded_files(uploaded_files, product_name):
    """Save uploaded files to a temporary session folder."""
    session_folder = os.path.join(BASE_INPUT_FOLDER, f"Web_Upload_{st.session_state.session_id}")
    if not os.path.exists(session_folder):
        os.makedirs(session_folder)
    
    saved_paths = []
    for uploaded_file in uploaded_files:
        file_path = os.path.join(session_folder, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        saved_paths.append(file_path)
    
    return saved_paths, session_folder

def clear_session_folder():
    """Clean up temporary upload folder."""
    import shutil
    session_folder = os.path.join(BASE_INPUT_FOLDER, f"Web_Upload_{st.session_state.session_id}")
    if os.path.exists(session_folder):
        shutil.rmtree(session_folder)

# --- Sidebar Configuration ---
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/gemini.png", width=80)
    st.title("⚙️ Settings")
    
    # Product Selection
    products = get_available_products()
    if not products:
        st.error("❌ No products found in Prompts folder!")
        st.stop()
    
    selected_product = st.selectbox(
        "📦 Select Product",
        products,
        help="Choose the product type you want to generate images for"
    )
    
    st.divider()
    
    # Variant Selection
    st.subheader("🎯 Poses to Generate")
    
    # Load available variants for this product
    prompt_path = os.path.join(BASE_PROMPT_FOLDER, selected_product)
    extra_tasks = utils.get_extra_tasks(prompt_path)
    
    # Front is always available
    generate_front = st.checkbox("Front View", value=True)
    
    # Dynamic variant checkboxes
    selected_variants = {}
    for task in extra_tasks:
        key = task["suffix"].replace("_", "")
        selected_variants[key] = st.checkbox(f"{key} View", value=True)
    
    st.divider()
    
    # Resolution
    resolution = st.selectbox(
        "📐 Resolution",
        ["1K", "2K", "4K"],
        index=0,
        help="Higher resolution = slower generation"
    )
    
    # Advanced Options (collapsed)
    with st.expander("🔧 Advanced Options"):
        st.info("These settings are for advanced users.")
        show_debug = st.checkbox("Show Debug Info", value=False)

# --- Main Content Area ---
st.title("✨ Gemini Auto Tool")
st.markdown("### Generate professional product images with AI")

# --- File Upload Section ---
st.markdown("---")
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📤 Upload Your Images")
    uploaded_files = st.file_uploader(
        "Drag and drop your product images here",
        type=["png", "jpg", "jpeg", "webp", "heic", "heif"],
        accept_multiple_files=True,
        help="Upload the raw product images you want to transform"
    )
    
    if uploaded_files:
        st.success(f"✅ {len(uploaded_files)} image(s) uploaded successfully!")
        
        # Preview thumbnails
        preview_cols = st.columns(min(len(uploaded_files), 4))
        for idx, (col, file) in enumerate(zip(preview_cols, uploaded_files[:4])):
            with col:
                img = Image.open(file)
                st.image(img, caption=file.name[:15] + "...", use_container_width=True)

with col2:
    st.subheader("📊 Status")
    
    # Session info
    st.metric("Session ID", st.session_state.session_id)
    st.metric("Product", selected_product)
    st.metric("Images Generated", len(st.session_state.generated_images))

# --- Generation Button ---
st.markdown("---")
generate_col1, generate_col2, generate_col3 = st.columns([1, 2, 1])

with generate_col2:
    if st.button("🚀 Generate Images", use_container_width=True, disabled=not uploaded_files):
        if not uploaded_files:
            st.warning("Please upload at least one image first!")
        else:
            st.session_state.processing = True
            st.session_state.generated_images = []
            
            # Save uploaded files
            saved_paths, session_folder = save_uploaded_files(uploaded_files, selected_product)
            
            # Load master prompt
            master_prompt_file = os.path.join(BASE_PROMPT_FOLDER, selected_product, "master_prompt.txt")
            master_prompt = utils.read_file(master_prompt_file)
            
            if not master_prompt:
                st.error(f"❌ Master prompt not found for {selected_product}")
                st.stop()
            
            # Create output folder
            product_output_folder = os.path.join(OUTPUT_FOLDER, selected_product)
            if not os.path.exists(product_output_folder):
                os.makedirs(product_output_folder)
            
            output_session_folder = utils.get_unique_folder(product_output_folder, f"Web_{st.session_state.session_id}")
            
            # Progress tracking
            total_steps = (1 if generate_front else 0) + sum(1 for v in selected_variants.values() if v)
            current_step = 0
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # --- Generate Front View ---
            if generate_front:
                status_text.text("🎨 Generating Front View...")
                
                front_path = saved_paths[0] if saved_paths else None
                if front_path:
                    result_img, error = api_client.fetch_image_from_api(
                        master_prompt, 
                        [front_path],
                        aspect_ratio="1:1",
                        image_size=resolution
                    )
                    
                    if result_img:
                        # Save front image
                        front_save_path = os.path.join(output_session_folder, "Front.jpg")
                        result_img.convert('RGB').save(front_save_path, quality=100)
                        st.session_state.current_front_image = front_save_path
                        st.session_state.generated_images.append(("Front", result_img, front_save_path))
                    else:
                        st.error(f"❌ Front generation failed: {error}")
                
                current_step += 1
                progress_bar.progress(current_step / total_steps)
            
            # --- Generate Variants ---
            for task in extra_tasks:
                key = task["suffix"].replace("_", "")
                if key in selected_variants and selected_variants[key]:
                    status_text.text(f"🎨 Generating {key} View...")
                    
                    prompt_text = utils.read_file(task["file"])
                    if prompt_text:
                        # Use front image + original as inputs
                        inputs = []
                        if st.session_state.current_front_image:
                            inputs.append(st.session_state.current_front_image)
                        if saved_paths:
                            inputs.append(saved_paths[0])
                        
                        result_img, error = api_client.fetch_image_from_api(
                            prompt_text,
                            inputs,
                            aspect_ratio=task["ratio"],
                            image_size=resolution
                        )
                        
                        if result_img:
                            variant_save_path = os.path.join(output_session_folder, f"{key}.jpg")
                            result_img.convert('RGB').save(variant_save_path, quality=100)
                            st.session_state.generated_images.append((key, result_img, variant_save_path))
                        else:
                            st.warning(f"⚠️ {key} generation failed: {error}")
                    
                    current_step += 1
                    progress_bar.progress(current_step / total_steps)
            
            status_text.text("✅ All images generated!")
            st.session_state.processing = False
            
            # Clean up temp folder
            # clear_session_folder()  # Uncomment to auto-clean
            
            st.rerun()

# --- Results Display ---
if st.session_state.generated_images:
    st.markdown("---")
    st.subheader("🖼️ Generated Images")
    
    # Display in grid
    num_cols = min(len(st.session_state.generated_images), 4)
    result_cols = st.columns(num_cols)
    
    for idx, (name, img, path) in enumerate(st.session_state.generated_images):
        with result_cols[idx % num_cols]:
            st.image(img, caption=name, use_container_width=True)
            
            # Download button for each image
            buf = io.BytesIO()
            img.convert('RGB').save(buf, format='JPEG', quality=100)
            st.download_button(
                label=f"📥 Download {name}",
                data=buf.getvalue(),
                file_name=f"{name}.jpg",
                mime="image/jpeg",
                key=f"download_{idx}"
            )
    
    # Download All button
    st.markdown("---")
    if st.button("📦 Download All as ZIP", use_container_width=True):
        import zipfile
        
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for name, img, path in st.session_state.generated_images:
                img_buffer = io.BytesIO()
                img.convert('RGB').save(img_buffer, format='JPEG', quality=100)
                zip_file.writestr(f"{name}.jpg", img_buffer.getvalue())
        
        st.download_button(
            label="💾 Click to Save ZIP",
            data=zip_buffer.getvalue(),
            file_name=f"generated_images_{st.session_state.session_id}.zip",
            mime="application/zip"
        )

# --- Footer ---
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #888;'>"
    "Made with ❤️ for SG Enterprise | Powered by Google Gemini"
    "</div>",
    unsafe_allow_html=True
)
