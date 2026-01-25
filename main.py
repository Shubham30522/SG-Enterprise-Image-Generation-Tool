
import os
import threading
import uuid
import tkinter as tk
import shutil
from tkinter import messagebox
from tkinter import ttk, filedialog
from PIL import Image, ImageTk

# Import from modular files
from config import BASE_INPUT_FOLDER, BASE_PROMPT_FOLDER, OUTPUT_FOLDER, API_KEY, CHROME_PROFILE, CHROME_URL
import utils
import api_client
import configure_prompts  # New Import

if not API_KEY:
    print("Error: API Key not found in .env file (checked via config.py).")

class Tooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event=None):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25

        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")

        label = tk.Label(self.tooltip, text=self.text, bg="#ffffe0", relief="solid", borderwidth=1, font=("Segoe UI", 9))
        label.pack()

    def hide_tooltip(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

class GeminiAutoToolGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Gemini Pipeline (5-Shot) - RC Imitation")
        self.root.minsize(600, 750)
        self.root.configure(bg="#f4f4f4")

        # Instance State (Replaces Globals)
        self.input_folder = None
        self.main_prompt_file = None
        self.extra_tasks = []

        self.sku_folders = []
        self.current_sku_images = []
        self.all_sku_images = []  # Store ALL images from SKU folder for batch variants
        self.current_index = 0
        self.current_generated_image = None
        self.is_processing = False
        self.current_batch_prompt = ""
        self.master_prompt = ""
        
        self.current_job_id = None # for checking thread validity
        self.pending_batch_args = None # State for Save/Next button toggle

        # Pose Selection Variables
        self.pose_vars = {}
        
        # Reference Image Variables
        self.ref_image_path = tk.StringVar()
        self.match_pose_var = tk.BooleanVar(value=False)
        self.match_bg_var = tk.BooleanVar(value=False)

        # Chrome Automation
        self.auto_desktop_var = tk.BooleanVar(value=False)

        # Initialize product list
        self.available_products = self.get_available_products()
        if not self.available_products:
             messagebox.showerror("Error", f"No products found in {BASE_PROMPT_FOLDER}.")
             root.destroy()
             return

        self.setup_gui_elements()
        
        # Load initial product context (defaults to first available)
        initial_product = self.available_products[0] if "shirt" not in self.available_products else "shirt"
        self.product_var.set(initial_product)
        self.load_product_context(initial_product)
        
        self.status_label.config(text="Select product, poses and click 'Start Processing' to begin.")

    def get_available_products(self):
        """Fetch latest product folders from input_images directory."""
        if not os.path.exists(BASE_INPUT_FOLDER):
            os.makedirs(BASE_INPUT_FOLDER)
            return []
        
        products = [d for d in os.listdir(BASE_INPUT_FOLDER) if os.path.isdir(os.path.join(BASE_INPUT_FOLDER, d))]
        return products

    def load_product_context(self, product_name):
        print(f"Loading context for: {product_name}")
        
        # Update Instance Paths (No Globals!)
        self.input_folder = os.path.join(BASE_INPUT_FOLDER, product_name)
        prompt_path = os.path.join(BASE_PROMPT_FOLDER, product_name)
        self.main_prompt_file = os.path.join(prompt_path, "master_prompt.txt")
        self.extra_tasks = utils.get_extra_tasks(prompt_path)
        
        # Ensure input folder exists
        if not os.path.exists(self.input_folder):
             os.makedirs(self.input_folder)
        
        # Reload Prompts
        self.master_prompt = utils.read_file(self.main_prompt_file)
        if not self.master_prompt:
             self.update_status(f"Warning: master_prompt.txt missing for {product_name}")
        
        # Reload SKUs
        self.load_input_files()
        
        # Reset Reset state
        self.current_index = 0
        self.current_generated_image = None
        self.current_batch_prompt = self.master_prompt # Default
        self.update_checkboxes() # Refresh dynamic checkboxes
        self.image_label.config(image="", text=f"Loaded {product_name}. Ready.")

    def setup_gui_elements(self):
        # --- Bottom Section: Status & Buttons ---
        self.status_label = tk.Label(self.root, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W, bg="white")
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X, ipady=2)

        btn_frame = tk.Frame(self.root, bg="#f4f4f4")
        btn_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=15)

        # Row 0
        self.save_btn = tk.Button(btn_frame, text="💾 Save & Auto-Gen 4", font=("Segoe UI", 12, "bold"), bg="#ddffdd", 
                                 command=self.save_and_next_action, state=tk.DISABLED, width=20)
        self.save_btn.grid(row=0, column=0, padx=5, pady=5)

        self.save_next_btn = tk.Button(btn_frame, text="💾 Save Front", font=("Segoe UI", 12, "bold"), bg="#ddffff", 
                                 command=self.save_and_gen_new_action, state=tk.NORMAL, width=20)
        self.save_next_btn.grid(row=0, column=1, padx=5, pady=5)

        # Row 1
        self.regen_btn = tk.Button(btn_frame, text="🔄 Regenerate Front", font=("Segoe UI", 12), bg="#ffdddd", 
                                  command=self.regenerate_action, state=tk.DISABLED, width=20)
        self.regen_btn.grid(row=1, column=0, padx=5, pady=5)

        self.skip_btn = tk.Button(btn_frame, text="⏭ Skip", font=("Segoe UI", 12), bg="#eeeeee", 
                                 command=self.skip_action, state=tk.DISABLED, width=20)
        self.skip_btn.grid(row=1, column=1, padx=5, pady=5)

        # Center buttons
        btn_frame.grid_columnconfigure(0, weight=1)
        btn_frame.grid_columnconfigure(1, weight=1)

        # --- Top Section: Header & Info ---
        header_frame = tk.Frame(self.root, bg="#f4f4f4")
        header_frame.pack(side=tk.TOP, fill=tk.X, pady=10)
        tk.Label(header_frame, text="Gemini 5-Shot Pipeline", font=("Segoe UI", 16, "bold"), bg="#f4f4f4").pack()
        
        # --- Configuration Row (Product & Resolution) ---
        config_frame = tk.Frame(header_frame, bg="#f4f4f4")
        config_frame.pack(pady=5)
        
        # Product Dropdown
        tk.Label(config_frame, text="Product:", bg="#f4f4f4", font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT, padx=5)
        self.product_var = tk.StringVar()
        self.product_combo = ttk.Combobox(config_frame, textvariable=self.product_var, values=self.available_products, state="readonly", width=12)
        self.product_combo.pack(side=tk.LEFT, padx=5)
        self.product_combo.bind("<<ComboboxSelected>>", self.on_product_change)

        # Auto-Tune Button
        self.tune_btn = tk.Button(config_frame, text="✨ Auto-Tune", bg="#eebbff", font=("Segoe UI", 9), 
                                  command=self.auto_tune_action, width=12)
        self.tune_btn.pack(side=tk.LEFT, padx=5)
        
        # Resolution Dropdown
        tk.Label(config_frame, text="Res:", bg="#f4f4f4", font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT, padx=5)
        self.resolution_var = tk.StringVar(value="1K")
        resolutions = ["1K", "2K", "4K"]
        self.res_combo = ttk.Combobox(config_frame, textvariable=self.resolution_var, values=resolutions, state="readonly", width=5)
        self.res_combo.pack(side=tk.LEFT, padx=5)
        self.res_combo.current(0) # Select 1K by default physically

        # Checkbox Frame
        self.checkbox_frame = tk.Frame(header_frame, bg="#f4f4f4")
        self.checkbox_frame.pack(pady=5)

        # "All" Checkbox
        self.all_poses_var = tk.BooleanVar(value=False)
        tk.Checkbutton(self.checkbox_frame, text="All", variable=self.all_poses_var, 
                      bg="#f4f4f4", font=("Segoe UI", 10, "bold"), 
                      command=self.toggle_all_poses).pack(side=tk.LEFT, padx=5)

        # Separator
        tk.Label(self.checkbox_frame, text="|", bg="#f4f4f4", fg="#ccc").pack(side=tk.LEFT, padx=2)
        
        # Dynamic Checkbox Frame (Container for generated poses)
        self.dynamic_check_frame = tk.Frame(self.checkbox_frame, bg="#f4f4f4")
        self.dynamic_check_frame.pack(side=tk.LEFT)

        # Initial placeholder update (will be overwritten by load_product_context)
        # self.update_checkboxes() # Not needed here as load_product_context calls it immediately after


        # Reference Image Section
        ref_frame = tk.Frame(header_frame, bg="#f4f4f4")
        ref_frame.pack(pady=5)
        
        tk.Label(ref_frame, text="Ref Image:", bg="#f4f4f4", font=("Segoe UI", 10)).pack(side=tk.LEFT, padx=5)
        self.ref_entry = tk.Entry(ref_frame, textvariable=self.ref_image_path, width=40, state="readonly")
        self.ref_entry.pack(side=tk.LEFT, padx=5)
        
        tk.Button(ref_frame, text="Browse", font=("Segoe UI", 9), command=self.browse_ref_image).pack(side=tk.LEFT, padx=5)
        
        tk.Checkbutton(ref_frame, text="Match Pose", variable=self.match_pose_var, bg="#f4f4f4").pack(side=tk.LEFT, padx=5)
        tk.Checkbutton(ref_frame, text="Match Background", variable=self.match_bg_var, bg="#f4f4f4").pack(side=tk.LEFT, padx=5)

        # Auto-Open Checkbox
        tk.Checkbutton(ref_frame, text="New Desktop & Open Chrome", variable=self.auto_desktop_var, bg="#f4f4f4", fg="blue").pack(side=tk.LEFT, padx=10)

        # Start Button
        self.start_btn = tk.Button(header_frame, text="▶ Start Processing", font=("Segoe UI", 11, "bold"), bg="#ccffcc", command=self.start_batch_action)
        self.start_btn.pack(pady=5)
        
        self.file_info_label = tk.Label(self.root, text="Waiting...", bg="#f4f4f4", font=("Segoe UI", 10))
        self.file_info_label.pack(side=tk.TOP, pady=2)
        
        self.file_info_label.pack(side=tk.TOP, pady=2)
        
        # Batch Status Frame
        status_frame = tk.Frame(self.root, bg="#f4f4f4")
        status_frame.pack(side=tk.TOP, pady=2)

        self.batch_status_label = tk.Label(status_frame, text="", bg="#f4f4f4", font=("Segoe UI", 9, "italic"), fg="#712123")
        self.batch_status_label.pack(side=tk.LEFT)
        
        # Error Icon (Hidden by default)
        self.error_icon = tk.Label(status_frame, text="⚠️", bg="#f4f4f4", fg="red", font=("Segoe UI", 12), cursor="hand2")
        self.error_tooltip = Tooltip(self.error_icon, "Error Details")
        # Don't pack it yet, only show on error

        # --- Middle Section: Canvas (Expandable) ---
        self.canvas_frame = tk.Frame(self.root, bg="#ddd", bd=2, relief=tk.RIDGE)
        self.canvas_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.canvas_frame.pack_propagate(False)
        
        self.image_label = tk.Label(self.canvas_frame, text="Loading...", bg="#ddd")
        self.image_label.pack(expand=True, fill=tk.BOTH)

        # Bind resize event
        self.canvas_frame.bind("<Configure>", self.on_canvas_resize)

    def toggle_all_poses(self):
        state = self.all_poses_var.get()
        for var in self.pose_vars.values():
            var.set(state)

    def on_product_change(self, event):
        selected_product = self.product_var.get()
        if selected_product:
            self.load_product_context(selected_product)

    def on_canvas_resize(self, event):
        if self.current_generated_image:
            self.display_image(self.current_generated_image)

    def update_status(self, message):
        self.status_label.config(text=message)
        self.root.update_idletasks()
        
    def update_batch_status(self, message):
        self.batch_status_label.config(text=message)
        self.root.update_idletasks()

    def browse_ref_image(self):
        file_path = filedialog.askopenfilename(
            title="Select Reference Image",
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.webp")]
        )
        if file_path:
            self.ref_image_path.set(file_path)

    def load_input_files(self):
        try:
            if not os.path.exists(self.input_folder):
                self.sku_folders = []
                self.file_info_label.config(text="Input folder missing.")
                return

            items = os.listdir(self.input_folder)
            # Filter for directories
            self.sku_folders = [d for d in items if os.path.isdir(os.path.join(self.input_folder, d))]
            if not self.sku_folders:
                self.file_info_label.config(text=f"No SKU folders found in {self.product_var.get()}.")
            else:
                self.file_info_label.config(text=f"Total SKUs ({self.product_var.get()}): {len(self.sku_folders)}")
        except FileNotFoundError:
             os.makedirs(self.input_folder)
             self.sku_folders = []

    def update_checkboxes(self):
        """Rebuilds checkboxes dynamically based on self.extra_tasks."""
        # Clear existing
        for widget in self.dynamic_check_frame.winfo_children():
            widget.destroy()
        
        self.pose_vars = {}
        
        # 1. Always Add Front
        var = tk.BooleanVar(value=False)
        self.pose_vars["Front"] = var
        tk.Checkbutton(self.dynamic_check_frame, text="Front", variable=var, bg="#f4f4f4", font=("Segoe UI", 10)).pack(side=tk.LEFT, padx=5)
        
        # 2. Add Dynamic Tasks
        for task in self.extra_tasks:
            # task suffix: "_Back" -> "Back"
            key = task["suffix"].replace("_", "")
            
            # Avoid duplicate Front if logic somehow includes it
            if key == "Front": 
                continue
                
            var = tk.BooleanVar(value=False)
            self.pose_vars[key] = var
            # Use task key as label
            tk.Checkbutton(self.dynamic_check_frame, text=key, variable=var, bg="#f4f4f4", font=("Segoe UI", 10)).pack(side=tk.LEFT, padx=5)


    def set_buttons_state(self, state):
        self.regen_btn.config(state=state)
        self.save_btn.config(state=state)
        self.save_next_btn.config(state=state)
        # SKIP button is priority - always enabled unless list empty or at end, 
        # but technically we can always allow skipping to check if there is next.
        # We'll control it separately, or just Force Enable it if state is DISABLED (processing)
        if state == tk.DISABLED:
            # When processing, we want Skip enabled
             self.skip_btn.config(state=tk.NORMAL)
        else:
            # When idle (state=NORMAL), it matches others
             self.skip_btn.config(state=state)

    def display_image(self, pil_image):
        canvas_width = self.canvas_frame.winfo_width()
        canvas_height = self.canvas_frame.winfo_height()
        # Handle case where window is initializing and size is 1x1
        if canvas_width <= 1 or canvas_height <= 1:
            return

        img_ratio = pil_image.width / pil_image.height
        canvas_ratio = canvas_width / canvas_height

        if img_ratio > canvas_ratio:
            new_width = canvas_width
            new_height = int(canvas_width / img_ratio)
        else:
            new_height = canvas_height
            new_width = int(canvas_height * img_ratio)

        if new_width > 0 and new_height > 0:
            pil_image_resized = pil_image.resize((new_width, new_height), Image.LANCZOS)
            tk_img = ImageTk.PhotoImage(pil_image_resized)
            self.image_label.config(image=tk_img, text="")
            self.image_label.image = tk_img

    # --- 1. FRONT IMAGE GENERATION ---

    def run_generation_thread(self, job_id):
        try:
            if not self.sku_folders:
                self.update_status("No SKU folders found.")
                return
    
            # 1. Early Job ID Check
            if self.current_job_id != job_id:
                print(f"DEBUG: Job {job_id} cancelled (stale). Current: {self.current_job_id}")
                return

            sku_name = self.sku_folders[self.current_index]
            sku_path = os.path.join(self.input_folder, sku_name)
            print(f"DEBUG: run_generation_thread processing index {self.current_index}: {sku_name}") # DEBUG
            
            # Get all valid images in the SKU folder
            valid_exts = ('.png', '.jpg', '.jpeg', '.heic', '.heif')
            sku_images_all = [os.path.join(sku_path, f) for f in os.listdir(sku_path) if f.lower().endswith(valid_exts)]
            
            # Store ALL SKU images for batch variant generation (Back, Side, Detail, etc.)
            self.all_sku_images = sku_images_all.copy()
            
            # STRICT INPUT SELECTION: [Front Image, Reference Image]
            # 1. Find Front Image
            front_img = next((img for img in sku_images_all if "front" in os.path.basename(img).lower()), None)
            
            # Fallback: If no explicit "Front" file, take the first image found
            if not front_img and sku_images_all:
                front_img = sku_images_all[0]
            
            self.current_sku_images = []
            if front_img:
                self.current_sku_images.append(front_img)

            # 2. Find Global Reference Image
            # This allows placing a single reference image in "input_images/Product" to be used by all SKUs
            product_level_files = [
                os.path.join(self.input_folder, f) 
                for f in os.listdir(self.input_folder) 
                if os.path.isfile(os.path.join(self.input_folder, f)) and f.lower().endswith(valid_exts)
            ]
            
            if product_level_files:
                # Find best match for reference image
                ref_image = next((f for f in product_level_files if "reference" in os.path.basename(f).lower()), None)
                
                # Fallback: Just take the first image if no "reference" keyword found
                if not ref_image:
                    ref_image = product_level_files[0]
                    
                print(f"DEBUG: Found global reference image: {ref_image}")
                self.current_sku_images.append(ref_image)
            
            # 2. Before Heavy Lifting Check
            if self.current_job_id != job_id: return

            if not self.current_sku_images:
                self.update_status(f"No images found in {sku_name}")
                self.root.after(0, lambda: messagebox.showerror("Error", f"No images found in {sku_name}"))
                return
    
            self.update_status(f"Generating Front View: {sku_name}...")
            self.update_batch_status("")
            
            # Call API with All Images in Folder
            if self.pose_vars["Front"].get():
                # Use current_batch_prompt which might have overrides
                prompt_to_use = self.current_batch_prompt if self.current_batch_prompt else self.master_prompt
                
                generated_pil_image = None
                error_msg = None

                while True:
                    # Check Cancel inside loop
                    if self.current_job_id != job_id:
                        print(f"DEBUG: Job {job_id} cancelled during retry loop.")
                        return

                    print(f"\n--- GENERATING FRONT VIEW ---")
                    print(f"Inputs ({len(self.current_sku_images)}):")
                    for inp in self.current_sku_images:
                        print(f"  - {os.path.basename(inp)}")

                    generated_pil_image, error_msg = api_client.fetch_image_from_api(prompt_to_use, self.current_sku_images, aspect_ratio="1:1", image_size=self.resolution_var.get())
                    
                    if generated_pil_image:
                        break # Success
                    
                    # Failure - Retry
                    print(f"DEBUG: Front Generation failed for {sku_name}. Retrying... Reason: {error_msg}")
                    self.update_status(f"Generation Failed ({error_msg}). Retrying Front View...")
                    import time
                    time.sleep(1) # Prevent tight loop spam

                # 3. Final Result Check
                if self.current_job_id != job_id:
                    print(f"DEBUG: Job {job_id} finished but cancelled. Discarding result.")
                    return

                self.root.after(0, lambda: self.handle_generation_result(generated_pil_image, error_msg))
            else:
                if self.current_job_id != job_id: return
                self.update_status("Front View Skipped (Checkbox unchecked).")
                # We treat this as "success" but with no image, so user can proceed to batch
                self.root.after(0, self.handle_skipped_front)
        
        except Exception as e:
            if self.current_job_id != job_id: return
            print(f"CRITICAL THREAD ERROR: {e}")
            import traceback
            traceback.print_exc()
            self.root.after(0, lambda: messagebox.showerror("Thread Error", str(e)))

    def handle_skipped_front(self):
        self.is_processing = False
        self.current_generated_image = None
        self.image_label.config(image="", text="Front View Skipped.\nClick Save/Next to process variants.")
        self.set_buttons_state(tk.NORMAL)
        self.error_icon.pack_forget()


    def handle_generation_result(self, pil_image, error_msg=None):
        self.is_processing = False
        if pil_image:
            self.current_generated_image = pil_image
            self.display_image(pil_image)
            self.update_status("Front View Ready. Click Save to generate variants.")
            self.set_buttons_state(tk.NORMAL)
            self.error_icon.pack_forget()
            
            # Ensure button is reset
            self.pending_batch_args = None
            self.save_next_btn.config(text="💾 Save Front")
        else:
            self.update_status("Generation Failed.")
            self.set_buttons_state(tk.NORMAL)
            
            # Show Error Icon
            if error_msg:
                self.error_icon.pack(side=tk.LEFT, padx=5)
                self.error_tooltip.text = error_msg # Update tooltip text
                messagebox.showerror("Generation Failed", f"Reason: {error_msg}")
            else:
                messagebox.showerror("Error", "Generation Failed (Unknown Reason).")

    def start_processing_next(self):
        if self.current_index < len(self.sku_folders):
            sku_name = self.sku_folders[self.current_index]
            self.file_info_label.config(text=f"Processing {self.current_index + 1} / {len(self.sku_folders)} : {sku_name}")
            
            self.set_buttons_state(tk.DISABLED)
            self.image_label.config(image="", text="Generating Front View...")
            self.is_processing = True
            
            # Reset Button State
            self.pending_batch_args = None
            self.save_next_btn.config(text="💾 Save Front")
            
            # New Job ID
            new_job_id = uuid.uuid4().hex
            self.current_job_id = new_job_id
            
            threading.Thread(target=self.run_generation_thread, args=(new_job_id,), daemon=True).start()
        else:
            self.update_status("All tasks completed.")
            self.image_label.config(image="", text="All Finished!")
            self.set_buttons_state(tk.DISABLED)
            messagebox.showinfo("Success", "All images processed!")

    # --- 2. BATCH VARIANT GENERATION (The New Logic) ---

    def save_current_front_image(self):
        """Helper to save the current front image. Returns (raw_paths, saved_path, base_name, output_folder) or None."""
        print("DEBUG: save_current_front_image called.") # DEBUG

        sku_name = self.sku_folders[self.current_index]
        
        product_output_folder = os.path.join(OUTPUT_FOLDER, self.product_var.get())
        if not os.path.exists(product_output_folder):
             os.makedirs(product_output_folder)

        sku_output_folder = utils.get_unique_folder(product_output_folder, sku_name)
        
        base_name = sku_name
        output_filename = f"{base_name}_Front.jpg"
        saved_front_path = os.path.join(sku_output_folder, output_filename)
        print(f"DEBUG: Attempting to save front image to: {saved_front_path}") # DEBUG
        
        try:
            if self.current_generated_image:
                self.current_generated_image.convert('RGB').save(saved_front_path, quality=100)
                print(f"Saved Front: {saved_front_path}")
            else:
                saved_front_path = None # Explicitly set to None if we didn't save it
            
            return self.all_sku_images, saved_front_path, base_name, sku_output_folder
        except Exception as e:
            messagebox.showerror("Save Error", str(e))
            return None

    def save_and_next_action(self):
        saved_data = self.save_current_front_image()
        if not saved_data: return
        
        raw_input_paths, saved_front_path, base_name, output_folder = saved_data

        # 2. Disable buttons and Start Batch Thread
        # 2. Disable buttons and Start Batch Thread
        self.set_buttons_state(tk.DISABLED)
        
        # New Job ID for Batch
        new_job_id = uuid.uuid4().hex
        self.current_job_id = new_job_id
        
        threading.Thread(target=self.run_batch_variants, args=(raw_input_paths, saved_front_path, base_name, output_folder, new_job_id), daemon=True).start()

    def save_and_gen_new_action(self):
        # Toggle Logic:
        # 1. If not saved yet (pending_batch_args is None) -> Save Front
        # 2. If saved (pending_batch_args has data) -> Start Batch

        if self.pending_batch_args is None:
            # Step 1: Save Front
            saved_data = self.save_current_front_image()
            if not saved_data: return

            self.pending_batch_args = saved_data
            
            # Update Button to "Generate Variants"
            self.save_next_btn.config(text="▶ Generate Variants")
            self.update_status("Front Saved. Click 'Generate Variants' to proceed.")

            # --- AUTO DESKTOP TRIGGER ---
            # --- AUTO DESKTOP TRIGGER ---
            if self.auto_desktop_var.get():
                try:
                    current_product = self.product_var.get()
                    self.update_status(f"Opening Chrome & Searching for '{current_product}'...")
                    # Run in a thread to prevent blocking GUI?
                    # Since it opens in new desktop, it might be fine to block briefly, but thread is safer.
                    # However, utils.create_desktop_and_open_chrome has sleeps, so definitely Thread.
                    
                    threading.Thread(target=utils.create_desktop_and_open_chrome, 
                                     args=(CHROME_PROFILE, CHROME_URL, current_product), 
                                     daemon=True).start()
                                     
                except Exception as e:
                    print(f"Auto-Desktop Failed: {e}")
                    messagebox.showwarning("Auto-Desktop Error", f"Failed to open Chrome: {e}")
            # ----------------------------
            
        else:
            # Step 2: Start Batch
            raw_input_paths, saved_front_path, base_name, output_folder = self.pending_batch_args
            
            # Disable buttons
            self.set_buttons_state(tk.DISABLED)
            
            # New Job ID for Batch
            new_job_id = uuid.uuid4().hex
            self.current_job_id = new_job_id
            
            # Reset state for next time
            self.pending_batch_args = None
            self.save_next_btn.config(text="💾 Save Front")

            threading.Thread(target=self.run_batch_variants, args=(raw_input_paths, saved_front_path, base_name, output_folder, new_job_id), daemon=True).start()

    def skip_action(self):
        # Immediate Cancel & Next
        print("DEBUG: SKIP clicked. Cancelling current job...")
        self.current_index += 1
        self.current_generated_image = None
        self.start_processing_next() # This will generate a NEW job_id, invalidating the old one

    def update_current_image(self, pil_image):
        self.current_generated_image = pil_image
        self.display_image(pil_image)

    def run_batch_variants(self, raw_paths, front_path, base_name, output_folder, job_id):
        """
        Generates 4 images sequentially using the RAW images and the FRONT image as inputs.
        """
        # Identify specific raw images based on filename keywords
        # Filter out Global Ref (which is in parent folder) to get only SKU-level raw images
        sku_raw_images = [p for p in raw_paths if os.path.dirname(p) != self.input_folder]
        
        raw_back_img = next((p for p in sku_raw_images if "back" in os.path.basename(p).lower()), None)
        raw_front_img = next((p for p in sku_raw_images if "front" in os.path.basename(p).lower()), None)
        raw_neck_img = next((p for p in sku_raw_images if "neck" in os.path.basename(p).lower()), None)
        raw_detail_img = next((p for p in sku_raw_images if "detail" in os.path.basename(p).lower()), None)
        raw_side_img = next((p for p in sku_raw_images if "side" in os.path.basename(p).lower()), None)
        
        # Fallback: if no specific "front"/"back" keyword, just take the first raw image
        fallback_raw = sku_raw_images[0] if sku_raw_images else None

        # Determine base inputs. If front_path is None (skipped), start with empty list
        # But per instruction, we strictly want [Generated Front, Raw Raw].
        
        total_tasks = len(self.extra_tasks)

        for i, task in enumerate(self.extra_tasks):
            # Check Cancel
            if self.current_job_id != job_id:
                print(f"DEBUG: Batch Job {job_id} cancelled during loop.")
                return

            # Check Checkbox
            pose_key = task["suffix"].replace("_", "")
            if pose_key in self.pose_vars and not self.pose_vars[pose_key].get():
                print(f"Skipping {pose_key} (checkbox unchecked)")
                continue

            prompt_text = utils.read_file(task["file"])
            if not prompt_text:
                print(f"Skipping {task['file']} (not found)")
                continue
            
            # --- STRICT INPUT LOGIC: [Generated Front] + [Specific Raw Image] ---
            current_inputs = [front_path] if front_path else []
            
            chosen_raw = None
            suffix = task["suffix"]
            
            if suffix == "_Back":
                chosen_raw = raw_back_img or raw_front_img or fallback_raw
            elif suffix == "_Neck":
                chosen_raw = raw_neck_img or raw_front_img or fallback_raw
            elif suffix == "_Detail":
                chosen_raw = raw_detail_img or raw_front_img or fallback_raw
            elif suffix == "_Side": # Often used for Folded view now
                chosen_raw = raw_side_img or raw_front_img or fallback_raw
            else:
                chosen_raw = raw_front_img or fallback_raw
            
            if chosen_raw:
                current_inputs.append(chosen_raw)
            
            # Update UI from thread
            self.batch_status_label.config(text=f"Generating {task['suffix'].replace('_', '').upper()} ({i+1}/{total_tasks})...")
            
            # Update UI from thread
            self.batch_status_label.config(text=f"Generating {task['suffix'].replace('_', '').upper()} ({i+1}/{total_tasks})...")
            
            # Generate with Retry
            result_img = None
            error_msg = None

            while True:
                if self.current_job_id != job_id:
                    print(f"DEBUG: Batch Job {job_id} cancelled during loop.")
                    return

                # DEBUG: Log exact inputs
                print(f"\n--- GENERATING {task['suffix'].replace('_', '').upper()} ---")
                print(f"Inputs ({len(current_inputs)}):")
                for inp in current_inputs:
                    print(f"  - {os.path.basename(inp)}")
                
                result_img, error_msg = api_client.fetch_image_from_api(prompt_text, current_inputs, aspect_ratio=task["ratio"], image_size=self.resolution_var.get())
                
                if result_img:
                    break # Success
                
                print(f"Failed to generate {task['file']}: {error_msg}. Retrying...")
                # Update UI to show retry status
                retry_msg = f"Retrying {task['suffix'].replace('_', '').upper()}..."
                if hasattr(self, 'root'):
                    self.root.after(0, lambda: self.batch_status_label.config(text=retry_msg))
                import time
                time.sleep(1)
            
            if result_img:
                # Auto Save
                suffix = task["suffix"]
                variant_filename = f"{base_name}{suffix}.jpg"
                save_path = os.path.join(output_folder, variant_filename)
                
                result_img.convert('RGB').save(save_path, quality=100)
                print(f"Saved Variant: {save_path}")
                
                # Check Cancel again before UI update
                if self.current_job_id != job_id: return
                self.root.after(0, self.update_current_image, result_img) 

        # 3. After batch finishes, move to next main image
        if self.current_job_id == job_id:
             self.root.after(0, self.finish_batch_and_next)

    def finish_batch_and_next(self):
        self.update_batch_status("Batch Complete.")
        self.current_index += 1
        self.current_generated_image = None
        self.start_processing_next()

    def start_batch_action(self):
        print("DEBUG: start_batch_action called.") # DEBUG
        # Validate selection
        if not any(var.get() for var in self.pose_vars.values()):
            messagebox.showwarning("Selection Required", "Please select at least one pose to generate.")
            return

        self.start_btn.config(state=tk.DISABLED)
        self.product_combo.config(state=tk.DISABLED)
        self.res_combo.config(state=tk.DISABLED)

        # --- Reference Image Analysis (Run Once) ---
        ref_path = self.ref_image_path.get()
        use_pose = self.match_pose_var.get()
        use_bg = self.match_bg_var.get()
        
        if ref_path and os.path.exists(ref_path) and (use_pose or use_bg):
            self.update_status(f"Analyzing Reference Image with Gemini 3 Pro...")
            self.root.update()
            
            analysis_results = api_client.analyze_reference_image(ref_path)
            if analysis_results:
                self.current_batch_prompt = api_client.inject_prompt_overrides(
                    self.master_prompt, 
                    analysis_results, 
                    inject_pose=use_pose, 
                    inject_bg=use_bg
                )
                print("DEBUG: Prompt updated with reference analysis.")
            else:
                print("Reference Analysis Failed. Using master prompt.")
                self.current_batch_prompt = self.master_prompt
        else:
            self.current_batch_prompt = self.master_prompt

        self.start_processing_next()

    def regenerate_action(self):
        if self.is_processing: return
        
        # CLEANUP: If we had a pending batch (meaning we just saved a front), delete it
        if self.pending_batch_args:
            try:
                # pending_batch_args = (raw_paths, saved_path, base_name, output_folder)
                folder_to_delete = self.pending_batch_args[3]
                if folder_to_delete and os.path.exists(folder_to_delete):
                    shutil.rmtree(folder_to_delete)
                    print(f"DEBUG: Cleanup - Deleted discarded folder: {folder_to_delete}")
            except Exception as e:
                print(f"Cleanup Error: {e}")

        self.update_status("Regenerating Front View...")
        self.set_buttons_state(tk.DISABLED)
        self.image_label.config(image="", text="Regenerating...")
        self.is_processing = True
        self.is_processing = True
        
        # Reset Button State
        self.pending_batch_args = None
        self.save_next_btn.config(text="💾 Save Front")

        # New Job ID for Regeneration
        new_job_id = uuid.uuid4().hex
        self.current_job_id = new_job_id
        threading.Thread(target=self.run_generation_thread, args=(new_job_id,), daemon=True).start()

    def reset_ui_state(self):
        self.set_buttons_state(tk.NORMAL)
        self.image_label.config(text="")
        
    def auto_tune_action(self):
        product_name = self.product_var.get()
        if not product_name:
            messagebox.showerror("Error", "Please select a product first.")
            return
            
        if messagebox.askyesno("Auto-Tune Prompts", f"This will analyze '{product_name}' images and OVERWRITE existing prompt files.\n\nAre you sure?"):
            self.set_buttons_state(tk.DISABLED)
            self.image_label.config(image="", text=f"Auto-Tuning '{product_name}'... Please wait.")
            
            threading.Thread(target=self.run_auto_tune_thread, args=(product_name,), daemon=True).start()

    def run_auto_tune_thread(self, product_name):
        try:
            status = configure_prompts.auto_tune_prompts(product_name)
            
            def success_ui():
                if status == "Success":
                    # RELOAD CONTEXT to ensure new prompts are used!
                    self.load_product_context(product_name)
                    messagebox.showinfo("Success", "Prompts have been Auto-Tuned & Reloaded!\n\nNew Style from Reference Image applied.\nReal Constraints from Raw Image applied.")
                else:
                    messagebox.showerror("Error", f"Auto-Tune Failed: {status}")
                self.reset_ui_state()
            
            self.root.after(0, success_ui)
            
        except Exception as e:
            print(f"Auto-Tune Error: {e}")
            err_msg = str(e)
            self.root.after(0, lambda: [messagebox.showerror("Error", err_msg), self.reset_ui_state()])

# --- Main Execution ---
if __name__ == "__main__":
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)
    root = tk.Tk()
    app = GeminiAutoToolGUI(root)
    root.mainloop()