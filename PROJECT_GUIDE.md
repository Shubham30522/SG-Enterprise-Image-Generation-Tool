# Project File Guide

This document describes the purpose of this repository, the high-level flow of the toolchain, and a concise file-by-file guide to help you understand and use the project.

## 🎯 Purpose & Goal

**Why this was built:**
The primary goal of this software is to create e-commerce-ready catalogue images for products that do not have production-ready photoshoots. By leveraging AI (Google Gemini and OpenAI ChatGPT), it circumvents the need for expensive and time-consuming physical photoshoots, enabling you to generate high-quality, professional product catalogs easily.

**What the software does:**
This repository serves as an internal toolkit that takes raw, unpolished product photos and converts them into consistent, e-commerce-ready images. The toolchain manages everything from prompts and API communication to image generation and output organization. It supports multiple interfaces tailored for different workflows: a Tkinter desktop GUI, a Streamlit web UI, and a FastAPI backend. Additionally, it features an optional Selenium-based automation layer for seamlessly publishing and cataloging the generated images to e-commerce platforms.

**High-level Flow (what happens end-to-end):**

1. Prepare inputs: place raw product images inside `input_images/<Product>/<SKU>/` and ensure prompts live in `Prompts/<Product>/` (a `master_prompt.txt` plus optional variant prompt `.txt` files).
2. Choose UI: run the desktop GUI (`main.py`) or open the Streamlit web UI (`web_app.py`) or call the FastAPI server (`server.py`) from a separate frontend.
3. The UI loads the `master_prompt.txt` and any variant prompts via `utils.get_extra_tasks()` and `utils.read_file()`.
4. When generation is requested, `api_client.generate_image()` routes the prompt and input images to either Google Gemini or OpenAI (GPT Image 2) based on user selection, and returns a PIL image object.
5. Generated images are saved under `output_images/<Product>/...` (unique folder names created with `utils.get_unique_folder`).
6. Optionally, `configure_prompts.auto_tune_prompts()` can analyze a reference and raw image using Gemini to create or update `master_prompt.txt` and variant prompt templates automatically.
7. If needed, `automation/script_executor.py` can run Selenium JSON scripts (in `automation/scripts/`) to automate browser tasks (e.g., Meesho cataloging).

---

## Quickstart / How to use

- Prerequisites:
  - Python 3.9+ (recommended).
  - Create a `.env` file in the repo root with `GOOGLE_API_KEY=<your_key>`, `OPENAI_API_KEY=<your_openai_key>` (optional), and optionally `MEESHO_EMAIL` / `MEESHO_PASSWORD` and `CHROME_PROFILE`.
  - Install Python dependencies (typical):

```powershell
pip install -r requirements.txt
# If you don't have a requirements.txt, install common needed packages:
pip install pillow requests python-dotenv fastapi uvicorn streamlit selenium openai
```

- Run the desktop GUI (Tkinter):

```powershell
python main.py
```

- Run the Streamlit web UI (single-machine web):

```powershell
streamlit run web_app.py
```

- Run the API server (for React/Vite frontend or remote use):

```powershell
uvicorn server:app --reload --host 127.0.0.1 --port 8000
```

- Use the automation scripts (Selenium): ensure ChromeDriver and Chrome are installed, then call from Python or via the GUI helper:

```python
from automation.script_executor import execute_script
execute_script('meesho_cataloging', profile='Default', url='https://seller.example')
```

---

## Files & What they do (concise, actionable)

- `main.py` — Desktop Tkinter app and primary local workflow orchestrator. Launches GUI, loads product prompts, selects SKUs, calls `api_client` to generate front + variant images, supports Auto-Tune and Chrome automation options.

- `web_app.py` — Streamlit-based web UI for single-machine usage. Lets users upload images, choose product prompts, and generate images via `api_client`. Stores results under `output_images/` in a session-specific folder.

- `server.py` — FastAPI backend wrapping generation logic and implementing job state tracking (SSE-ready). Designed to be used with a React/Vite frontend (in `web/`) or other HTTP clients. Ensures prompt/input/output directories exist at startup.

- `api_client.py` — API interface. Key functions:
  - `generate_image(prompt, image_paths, aspect_ratio, image_size, provider)` — unified dispatcher that routes to Gemini or OpenAI.
  - `fetch_image_from_api(...)` — raw REST client for Google Gemini.
  - `fetch_image_from_openai(...)` — uses `openai` Python SDK for ChatGPT.
  - `analyze_reference_image(image_path)` — ask Gemini to describe pose and environment.
  - `inject_prompt_overrides(base_prompt, overrides, inject_pose, inject_bg)` — helper to merge analysis outputs into existing prompts.

- `configure_prompts.py` — Auto-tune and prompt generation utilities. Analyzes style + raw product images with Gemini, generates `master_prompt.txt` and a set of variant prompt files (e.g., `back.txt`, `side.txt`, `neck.txt`, `detail.txt`). Useful for quickly creating consistent prompt templates per product.

- `utils.py` — Small helpers used across the project:
  - `read_file(filepath)` — safe read.
  - `get_unique_filename(...)` / `get_unique_folder(...)` — avoid overwriting outputs.
  - `get_extra_tasks(product_path)` — read prompt `.txt` files (excluding master) and return variant definitions used by UIs.
  - `create_desktop_and_open_chrome(profile, url, ...)` — helper that triggers `automation.script_executor.execute_script()`.

- `automation/script_executor.py` — Loads JSON step scripts from `automation/scripts/` and executes them with Selenium. Supports actions like `goToURL`, `clickElement`, `inputText`, `waitUntilVisible`, and has a built-in login helper for Meesho.

- `automation/scripts/*.json` — Example automation flows (e.g., `meesho_cataloging.json`). Edit or add scripts to automate repetitive browser tasks.

- `Prompts/<Product>/master_prompt.txt` — The primary prompt used to generate the front view for a product. Variant prompt files (e.g., `back.txt`) live alongside it and reference the generated Front image when producing variants.

- `input_images/<Product>/<SKU>/...` — Place your raw images here. Prefer consistent naming (e.g., include `front` or `reference` in filenames to help heuristics), but the tool will try sensible defaults.

- `output_images/` — Destination for all generated images. The UI and web app create unique folders for sessions and product runs.

---

## Notes, Tips & Gotchas

- API Keys: Set `GOOGLE_API_KEY` and `OPENAI_API_KEY` in `.env`. If a key is missing, the respective provider toggle will be automatically disabled in the React UI.
- HEIC support: `api_client` tries to import `pillow-heif`; without it HEIC/HEIF files will be skipped or require conversion.
- Prompt editing: `Prompts/<Product>/master_prompt.txt` is authoritative — edit it to tune Front outputs. Variant templates in `configure_prompts.py` show expected content for detail/back/side variants.
- Automation: Selenium scripts will kill existing Chrome instances before launching a profile. Use a dedicated profile (or specify a different `CHROME_PROFILE`) to avoid losing browser state.
- Web frontend: there's a `web/` folder containing a Vite-based frontend (React). The FastAPI `server.py` is intended to be the backend for that frontend.

---

If you'd like, I can now:

- run a more thorough scan and produce a shorter `README.md` with the exact commands to install dependencies and run each UI, or
- update the `requirements.txt` and add a `Makefile`/`run` scripts for convenience.
