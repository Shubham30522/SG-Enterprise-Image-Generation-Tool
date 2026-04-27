# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Gemini Auto Tool is an internal toolkit for **SG Enterprise** that converts raw product photos into e-commerce-ready catalogue images using the Google Gemini API (`gemini-3-pro-image-preview`) or OpenAI ChatGPT (`gpt-image-2`). It eliminates the need for professional photoshoots by generating consistent front, back, side, neck, and detail views from a single raw product image plus a style reference.

The system supports three UI surfaces backed by shared Python modules:
- **Desktop GUI** (`main.py`) — Tkinter app, the original primary workflow
- **Streamlit Web UI** (`web_app.py`) — single-machine web interface
- **React + FastAPI** (`server.py` + `web/`) — client-server architecture with SSE job streaming; this is the actively developed interface

## Running the Application

```bash
# Desktop GUI (Tkinter)
python main.py

# Streamlit web UI
python -m streamlit run web_app.py --server.headless true

# React + FastAPI (two terminals, or use start_web.bat on Windows)
python -m uvicorn server:app --reload --port 8000   # backend
cd web && npm run dev                                 # frontend at :5173

# Build React frontend for production
cd web && npm run build
```

The `start_web.bat` script launches both backend and frontend together on Windows.

## Architecture

### Data flow

1. Raw images go in `input_images/<Product>/<SKU>/` (e.g. `input_images/shirt/Yellow/`)
2. Prompts live in `Prompts/<Product>/` — `master_prompt.txt` (front view) plus variant files (`back.txt`, `side.txt`, `neck.txt`, `detail.txt`, etc.)
3. `api_client.fetch_image_from_api()` sends prompt + base64-encoded input images to the Gemini REST API and returns a PIL Image
4. Generated images are saved under `output_images/<Product>/` in uniquely-named folders

### Core Python modules

| File | Role |
|---|---|
| `config.py` | Loads `.env`, exports API keys (`API_KEY`, `OPENAI_API_KEY`), folder paths (`BASE_INPUT_FOLDER`, `BASE_PROMPT_FOLDER`, `OUTPUT_FOLDER`), and Meesho credentials |
| `api_client.py` | API client module — `generate_image()` acts as the dispatcher routing to either `fetch_image_from_api()` (Gemini) or `fetch_image_from_openai()` (ChatGPT). Also handles `analyze_reference_image()` (via Gemini) and `inject_prompt_overrides()` |
| `utils.py` | Helpers — `read_file()`, `get_unique_folder()`, `get_extra_tasks()` (discovers variant prompt files for a product) |
| `configure_prompts.py` | Auto-tune: analyzes a style reference + raw image via Gemini to generate `master_prompt.txt` and variant templates (`MASTER_PROMPT_TEMPLATE`, `VARIANT_TEMPLATES`) |
| `server.py` | FastAPI backend — REST + SSE endpoints, `JobState` class for async generation tracking, serves the React frontend |
| `web_app.py` | Streamlit UI — standalone web interface |
| `main.py` | Tkinter desktop GUI |

### React frontend (`web/`)

React 19 + Vite + Tailwind CSS 4. The Vite dev server proxies `/api/*` to `localhost:8000` (FastAPI).

Key components:
- `App.jsx` — main state management, page routing (`generation` / `product-manager`)
- `Sidebar.jsx` — product/SKU/pose selection, reference image upload
- `api/client.js` — all fetch calls to the FastAPI backend, SSE subscription via `subscribeToJob()`

### Prompt conventions

- Each product has a `Prompts/<Product>/master_prompt.txt` for the front view
- Variant prompt files (e.g. `back.txt`, `side.txt`) reference the generated front image and describe a different angle
- `utils.get_extra_tasks()` discovers variant files by listing `.txt` files excluding `master_prompt.txt`, sorted by priority: back, side, neck, detail, waistband, hem
- Prompt sections like `Model Pose:`, `Environment Physics:`, `Lighting Logic:`, `Lens Reasoning:` are used as markers for `inject_prompt_overrides()` to splice in reference analysis

### Automation layer

`automation/script_executor.py` runs Selenium-driven JSON scripts (in `automation/scripts/`) for e-commerce platform tasks like Meesho catalogue uploading. Requires ChromeDriver and kills existing Chrome instances before launching.

## Environment

Requires a `.env` file at repo root:
```
GOOGLE_API_KEY=<your-gemini-api-key>
OPENAI_API_KEY=<your-openai-api-key>
DEFAULT_AI_PROVIDER="gemini"
CHROME_PROFILE="Default"
CHROME_URL="https://..."
MEESHO_EMAIL=...
MEESHO_PASSWORD=...
```

Only `GOOGLE_API_KEY` and/or `OPENAI_API_KEY` are required for image generation. The UI will dynamically disable providers if their keys are missing. The Meesho/Chrome variables are only needed for Selenium automation.

## Key Patterns

- **Multi-Provider Architecture**: Image generation is handled by a unified dispatcher (`generate_image` in `api_client.py`), which routes requests based on the user's selected provider to either the raw REST Gemini client or the `openai` Python SDK.
- `server.py` uses `JobState` with `threading.Event` and a list of SSE events to stream generation progress to the React frontend
- Image generation returns `(PIL.Image, None)` on success or `(None, error_string)` on failure — callers must check the error return
- HEIC/HEIF support is optional and depends on `pillow-heif` being installed
- Output folders use auto-incrementing suffixes (`Yellow`, `Yellow_1`, `Yellow_2`) via `utils.get_unique_folder()` to avoid overwriting previous runs
