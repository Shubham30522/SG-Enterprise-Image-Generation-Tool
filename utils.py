
import os

# ─── Cloud Storage Import ────────────────────────────────────────────────
try:
    from storage_client import storage as _cloud_storage
    CLOUD_AVAILABLE = True
except Exception:
    _cloud_storage = None
    CLOUD_AVAILABLE = False


# ─── Text File Reading ───────────────────────────────────────────────────

def read_file(filepath):
    """Reads a text file safely from local disk."""
    if not os.path.exists(filepath):
        return None
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read().strip()


def read_file_cloud(cloud_path):
    """Reads a text file from Supabase Storage."""
    if not CLOUD_AVAILABLE:
        return None
    content = _cloud_storage.download_text(cloud_path)
    return content.strip() if content else None


# ─── Unique Naming ───────────────────────────────────────────────────────

def get_unique_filename(directory, base_name):
    """Returns a unique filename (appending counter) if file exists."""
    filename = f"{base_name}.jpg"
    counter = 1
    while os.path.exists(os.path.join(directory, filename)):
        filename = f"{base_name}_{counter}.jpg"
        counter += 1
    return filename


def get_unique_folder(base_dir, folder_name):
    """
    Creates a unique folder path. If folder_name exists, appends _1, _2, etc.
    Returns the absolute path of the created folder.
    """
    folder_path = os.path.join(base_dir, folder_name)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        return folder_path
    
    counter = 1
    while True:
        new_folder_name = f"{folder_name}_{counter}"
        new_folder_path = os.path.join(base_dir, new_folder_name)
        if not os.path.exists(new_folder_path):
            os.makedirs(new_folder_path)
            return new_folder_path
        counter += 1


def get_unique_folder_cloud(base_path, folder_name):
    """
    Returns a unique cloud folder path.
    Checks existing 'folders' (prefixes) in Supabase to avoid collisions.
    """
    if not CLOUD_AVAILABLE:
        return f"{base_path}/{folder_name}"
    
    target = f"{base_path}/{folder_name}"
    items = _cloud_storage.list_directory(target)
    if not items:
        return target
    
    counter = 1
    while True:
        new_target = f"{base_path}/{folder_name}_{counter}"
        items = _cloud_storage.list_directory(new_target)
        if not items:
            return new_target
        counter += 1


# ─── Variant Task Discovery ─────────────────────────────────────────────

def get_extra_tasks(product_path):
    """
    Returns list of variant tasks based on files present in the folder.
    Scans for 'prompt_*.txt' files (excluding master_prompt.txt).
    """
    tasks = []
    if not os.path.exists(product_path):
        return tasks
        
    # Get all text files (excluding master)
    files = [f for f in os.listdir(product_path) if f.lower().endswith(".txt") and f.lower() != "master_prompt.txt"]
    
    # Priority Order for consistent display
    priority = ["back", "side", "neck", "detail", "waistband", "hem"]
    
    # Sort files: priority matching first, then alphabetical
    def sort_key(fname):
        # Remove extension to get "name"
        name = fname.lower().replace(".txt", "")
        # Handle transitional cases where "prompt_" might still exist during migration, or just strip it if user forgot
        name = name.replace("prompt_", "") 
        
        if name in priority:
            return priority.index(name)
        return 999
    
    files.sort(key=sort_key)

    for f in files:
        # Extract suffix key for UI
        # e.g. "waistband.txt" -> "_Waistband"
        # e.g. "folded_stack.txt" -> "_FoldedStack"
        
        name_part = f[:-4] # remove .txt
        if name_part.lower().startswith("prompt_"):
             name_part = name_part[7:]

        suffix_key = "_" + name_part.title().replace(" ", "").replace("_", "")
        
        tasks.append({
            "file": os.path.join(product_path, f),
            "suffix": suffix_key,
            "ratio": "1:1"
        })
            
    return tasks


def get_extra_tasks_cloud(prompts_cloud_path):
    """
    Cloud version: Returns variant tasks by listing .txt files in a Supabase folder.
    prompts_cloud_path: e.g. 'prompts/ProductName'
    """
    if not CLOUD_AVAILABLE:
        return []

    tasks = []
    items = _cloud_storage.list_directory(prompts_cloud_path)
    
    # Filter to .txt files, exclude master_prompt.txt
    txt_files = [
        item["name"] for item in items
        if item.get("name", "").lower().endswith(".txt")
        and item.get("name", "").lower() != "master_prompt.txt"
    ]
    
    priority = ["back", "side", "neck", "detail", "waistband", "hem"]
    
    def sort_key(fname):
        name = fname.lower().replace(".txt", "").replace("prompt_", "")
        if name in priority:
            return priority.index(name)
        return 999
    
    txt_files.sort(key=sort_key)
    
    for f in txt_files:
        name_part = f[:-4]
        if name_part.lower().startswith("prompt_"):
            name_part = name_part[7:]
        
        suffix_key = "_" + name_part.title().replace(" ", "").replace("_", "")
        cloud_file_path = f"{prompts_cloud_path}/{f}"
        
        tasks.append({
            "file": cloud_file_path,  # This is a cloud path now
            "suffix": suffix_key,
            "ratio": "1:1"
        })
    
    return tasks


