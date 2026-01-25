# Project File Guide

This document lists every file in the current project, explaining why it is needed, its specific use, and where it is utilized.

## Core Application Files

### `main.py`
**The Heart of the App**
- **Why it is needed:** This is the primary entry point for the "Gemini Pipeline" GUI.
- **Use & Functionality:**
  - Launches the Tkinter Graphical User Interface.
  - Orchestrates the entire image generation workflow (Front -> Variants).
  - Handles threading for background tasks (generation, auto-tuning).
  - Manages file input/output selection and displaying images.
- **Where it is used:** Run directly to start the application: `python main.py`

### `api_client.py`
**API Communication**
- **Why it is needed:** Keeps the API logic separate from the GUI code for cleaner architecture.
- **Use & Functionality:**
  - Sends requests to Google's Gemini API.
  - Handles image encoding to Base64.
  - Manages `gemini-3-pro-image-preview` for generation and `gemini-3-pro-preview` for analysis.
  - Includes logic for analyzing reference images to extract pose/background.
- **Where it is used:** Used by `main.py` for all generation tasks and `configure_prompts.py` logic.

### `config.py`
**Configuration Management**
- **Why it is needed:** Centralizes constants and environment loading.
- **Use & Functionality:**
  - Loads the `GOOGLE_API_KEY` from the `.env` file.
  - Defines absolute paths for `input_images`, `Prompts`, and `output_images` directories to prevent path errors.
- **Where it is used:** Imported by `main.py`, `api_client.py`, `configure_prompts.py`.

### `utils.py`
**Shared Utilities**
- **Why it is needed:** specific helper functions to avoid code duplication.
- **Use & Functionality:**
  - `read_file`: Safely reads text files.
  - `get_unique_folder` / `get_unique_filename`: Ensures no files are overwritten by adding counters (e.g., `image_1.jpg`).
  - `get_extra_tasks`: Defines the standard variant list (Back, Side, Neck, Detail) and their prompt mapping.
- **Where it is used:** Imported by `main.py`.

### `configure_prompts.py`
**Auto-Tuning Logic**
- **Why it is needed:** Powers the "Auto-Tune" feature in the GUI.
- **Use & Functionality:**
  - implementation of the `auto_tune_prompts` function.
  - Analyzes a Reference Image for style and a Raw Image for construction details.
  - Automatically updates text files in the `Prompts/` folder with extracted insights.
- **Where it is used:** Imported by `main.py` when the "Auto-Tune" button is clicked.

---

## Standalone / Utility Scripts

### `setup_test_product.py`
**Testing Setup**
- **Why it is needed:** Quickly resets a test environment.
- **Use & Functionality:**
  - Copies images and prompts from a source folder (e.g., `dress`) to a destination (e.g., `Dress - Flat lay`).
  - Renames specific files to standard names (e.g., `REFERENCE IMAGE.png`) to ensure the tool can find them.
- **Where it is used:** Run manually to prepare a clean test state: `python setup_test_product.py`

---

## Configuration & Data Files

### `.env`
- **Purpose**: Security.
- **Use**: Stores sensitive credentials like `GOOGLE_API_KEY` so they aren't hardcoded in the scripts.

### `.gitignore`
- **Purpose**: Version Control.
- **Use**: Tells Git which files to ignore (e.g., `__pycache__`, local configs, large image folders).

---

## Directories

### `Prompts/`
- **Purpose**: Prompt Management.
- **Content**: Stores folders for each product type (e.g., `shirt`, `dress`). Each folder contains `master_prompt.txt` and variant prompts (`_back`, `_side`, etc.).

### `input_images/`
- **Purpose**: Input Data.
- **Content**: Stores the raw images to be processed. Organized by Product -> SKU -> Images.

### `output_images/`
- **Purpose**: Results.
- **Content**: The destination for all AI-generated images.

### `Backup-Random/`
- **Purpose**: Storage.
- **Content**: A place to store random backup files or experiments that shouldn't clutter the main root.

### `__pycache__/`
- **Purpose**: Performance.
- **Content**: Automatically created by Python. Contains compiled bytecode (`.pyc` files) to make scripts load faster.
