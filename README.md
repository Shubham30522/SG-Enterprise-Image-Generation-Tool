<div align="center">

# 🖼️ Shotloom

### AI-Powered E-Commerce Image Generation Platform

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-19-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://react.dev)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)
[![Deployment](https://img.shields.io/badge/Deployed-Vercel-000?style=for-the-badge&logo=vercel)](https://sg-enterprise-image-generatio-git-2e0d8a-shubham30522s-projects.vercel.app/)

**Transform raw product photos into professional, e-commerce-ready catalogue images using AI — no photoshoot required.**

[Live Demo](https://sg-enterprise-image-generatio-git-2e0d8a-shubham30522s-projects.vercel.app/) · [Report Bug](.github/ISSUE_TEMPLATE/bug_report.md) · [Request Feature](.github/ISSUE_TEMPLATE/feature_request.md)

</div>

---

## 🚀 Overview

Shotloom is an AI-driven automation platform built by **SG Enterprise** that eliminates the need for expensive physical photoshoots. It takes a single raw product photo and generates consistent, multi-angle catalogue images (front, back, side, neck, detail, waistband, hem) using advanced generative AI models.

### The Problem

Independent sellers on platforms like **Meesho** and **Flipkart** spend ₹2,000–₹10,000 per product on professional photoshoots. This cost barrier prevents catalogue scaling and directly impacts revenue potential.

### Our Solution

By leveraging **Google Gemini Pro Vision** and **OpenAI GPT Image 2**, we reduce cataloguing costs by **up to 90%** and compress time-to-market from **days to minutes**.

---

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| 🤖 **Multi-Provider AI** | Seamless switching between Google Gemini and OpenAI GPT Image 2 |
| 🧠 **Claude Prompt Gen** | Production-grade prompt generation using the v2 skill framework via Claude 3.5 Sonnet on Vertex AI |
| 📸 **Multi-Angle Generation** | Auto-generates front, back, side, neck, detail, waistband, hem, and custom views |
| ⚡ **Real-Time Streaming** | Server-Sent Events (SSE) for live generation progress |
| 🎨 **Smart Prompt Engineering** | Auto-analyzes reference images to generate optimal prompts |
| 🔧 **Product Management** | Full CRUD operations for products, SKUs, and prompt templates |
| 🌐 **Cloud Storage** | Supabase integration for persistent image storage |
| 📱 **Responsive UI** | Modern React 19 interface with Tailwind CSS 4 |

---

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                   FRONTEND (React 19 + Vite)                 │
│                                                              │
│   ┌──────────┐  ┌───────────────┐  ┌──────────────────────┐  │
│   │ Sidebar  │  │  Generation   │  │  Product Manager     │  │
│   │ (Select) │  │  (SSE Stream) │  │  (CRUD Operations)   │  │
│   └──────────┘  └───────────────┘  └──────────────────────┘  │
└───────────────────────┬──────────────────────────────────────┘
                        │ REST API + SSE
┌───────────────────────▼──────────────────────────────────────┐
│                 BACKEND (FastAPI + Python)                    │
│                                                              │
│   ┌─────────────┐  ┌──────────────┐  ┌────────────────────┐  │
│   │ api_client  │  │  server.py   │  │ configure_prompts  │  │
│   │ (Dispatcher)│  │  (Job State) │  │ (Auto-Tune Engine) │  │
│   └──────┬──────┘  └──────────────┘  └────────────────────┘  │
│          │                                                    │
│   ┌──────▼───────────────────────────────────┐               │
│   │        AI Provider Dispatcher            │               │
│   │  ┌──────────────┐  ┌──────────────────┐  │               │
│   │  │ Google Gemini │  │  OpenAI GPT      │  │               │
│   │  │ (Pro Vision)  │  │  (Image 2)       │  │               │
│   │  └──────────────┘  └──────────────────┘  │               │
│   └──────────────────────────────────────────┘               │
└───────────────────────┬──────────────────────────────────────┘
                        │
┌───────────────────────▼──────────────────────────────────────┐
│                        STORAGE LAYER                         │
│                                                              │
│          ┌──────────────┐          ┌────────────┐            │
│          │  Supabase    │          │  Local FS  │            │
│          │  (Cloud)     │          │  (Dev)     │            │
│          └──────────────┘          └────────────┘            │
└──────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | React 19, Vite, Tailwind CSS 4 | Modern responsive UI |
| **Backend** | Python 3.9+, FastAPI, Uvicorn | REST API + SSE streaming |
| **AI / ML** | Google Gemini Pro Vision, OpenAI GPT Image 2 | Image generation & analysis |
| **Storage** | Supabase (prod), Local filesystem (dev) | Generated image persistence |
| **Deployment** | Vercel (frontend), Render (backend) | Production hosting |

---

## ⚡ Quick Start

### Prerequisites

- Python 3.9+
- Node.js 18+
- Google Gemini API key and/or OpenAI API key

### 1. Clone & Install

```bash
git clone https://github.com/Shubham30522/SG-Enterprise-Image-Generation-Tool.git
cd SG-Enterprise-Image-Generation-Tool

# Backend dependencies
pip install -r requirements.txt

# Frontend dependencies
cd web && npm install && cd ..
```

### 2. Configure Environment

Create a `.env` file in the project root:

```env
# Google Cloud Vertex AI (Gemini Image Gen & Claude Prompt Gen)
GCP_PROJECT_ID=your_gcp_project_id
GCP_LOCATION=global                        # Required for Gemini 3 Preview
GCP_REGION=us-east5                        # Regional endpoint for Claude
CLAUDE_MODEL_ID=claude-sonnet-4-6          # Default: claude-sonnet-4-6

# OpenAI API Key (Optional, for ChatGPT / GPT Image 2)
OPENAI_API_KEY=your_openai_api_key
DEFAULT_AI_PROVIDER="gemini"               # or "chatgpt"

# Supabase Storage Configuration
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
SUPABASE_BUCKET=app-storage                # Optional, default: app-storage
```

Authenticate with Google Cloud to set up Application Default Credentials (ADC) for Vertex AI access:

```bash
gcloud auth application-default login
```

### 3. Run

```bash
# Option A: Both backend + frontend (Windows)
start_web.bat

# Option B: Manual (any OS)
# Terminal 1 — Backend
uvicorn server:app --reload --port 8000

# Terminal 2 — Frontend
cd web && npm run dev
```

The app will be available at `http://localhost:5173`

---

## 📂 Project Structure

```
├── server.py              # FastAPI backend — REST + SSE endpoints
├── api_client.py          # AI provider dispatcher (Gemini / OpenAI)
├── config.py              # Environment configuration loader
├── configure_prompts.py   # Auto-tune prompt generation engine
├── utils.py               # Shared utility functions
├── storage_client.py      # Supabase cloud storage integration
├── requirements.txt       # Python dependencies
│
├── web/                   # React frontend
│   ├── src/
│   │   ├── App.jsx        # Main application with state management
│   │   ├── components/    # Reusable UI components
│   │   └── api/           # API client & SSE subscription
│   ├── package.json
│   └── vite.config.js     # Vite config with API proxy
│
├── Prompts/               # Product prompt templates
│   └── <Product>/
│       ├── master_prompt.txt   # Front view prompt
│       ├── back.txt            # Back view variant
│       ├── side.txt            # Side view variant
│       └── ...                 # Additional variants
│
├── .github/               # GitHub configuration
│   ├── workflows/         # CI/CD pipelines
│   ├── ISSUE_TEMPLATE/    # Bug & feature templates
│   └── PULL_REQUEST_TEMPLATE.md
│
└── input_images/          # Raw product photos (not tracked)
```

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/providers` | Get status of available/configured AI providers |
| `GET` | `/api/products` | List all available products |
| `POST` | `/api/products` | Create a new product |
| `DELETE` | `/api/products/{product_name}` | Delete a product and its content |
| `GET` | `/api/products/{product_name}/skus` | List SKUs for a product |
| `POST` | `/api/products/{product_name}/skus` | Add a SKU to a product |
| `DELETE` | `/api/products/{product_name}/skus/{sku_name}` | Delete a SKU from a product |
| `GET` | `/api/products/{product_name}/poses` | List available poses (front, back, side, etc.) |
| `GET` | `/api/products/{product_name}/prompts` | Read all prompt files for a product |
| `POST` | `/api/products/{product_name}/prompts` | Update prompt files for a product |
| `POST` | `/api/products/{product_name}/{sku_name}/upload` | Upload raw garment images to a SKU |
| `GET` | `/api/products/{product_name}/sku/{sku_name}/images` | List raw SKU images |
| `POST` | `/api/upload/reference` | Upload a style reference image |
| `POST` | `/api/analyze-reference` | Analyze pose & style of reference image |
| `POST` | `/api/generate/start` | Start generating front-view catalog image (tracked) |
| `POST` | `/api/generate/save-and-variants` | Save front image and generate variants (tracked) |
| `POST` | `/api/generate/save-front` | Save a generated front image |
| `POST` | `/api/generate/cancel/{job_id}` | Cancel an active generation job |
| `GET` | `/api/generate/stream/{job_id}` | SSE stream for real-time generation progress |
| `POST` | `/api/auto-tune` | Auto-generate prompt files via Gemini reference analysis |
| `GET` | `/api/claude-status` | Check if Claude (GCP Vertex AI) is configured and available |
| `POST` | `/api/generate-prompts-claude` | Generate production-grade prompts via Claude Vertex AI |
| `GET` | `/api/download/{product_name}/{folder_name}` | Download generated images batch as a ZIP file |

---

## 🚢 Deployment

### Frontend (Vercel)

The React frontend is deployed on Vercel with automatic deployments from the `master` branch.

```bash
# Build for production
cd web && npm run build
```

### Backend (Render)

The FastAPI backend runs on Render or Azure App Service with the following environment variables:

| Variable | Required | Description |
|----------|----------|-------------|
| `GCP_PROJECT_ID` | Yes* | Google Cloud project ID (for Vertex AI APIs) |
| `GCP_LOCATION` | No | Google Cloud region for Gemini (default: `us-central1`, set to `global` for Gemini 3 Preview) |
| `GCP_REGION` | No | Google Cloud region for Claude prompt generator (default: `us-east5`) |
| `CLAUDE_MODEL_ID` | No | Claude model name (default: `claude-sonnet-4-6`) |
| `OPENAI_API_KEY` | No* | OpenAI API key for GPT Image 2 provider |
| `DEFAULT_AI_PROVIDER` | No | Default provider: `gemini` or `chatgpt` |
| `SUPABASE_URL` | Yes | Supabase project URL for cloud image storage |
| `SUPABASE_KEY` | Yes | Supabase anon key for cloud image storage |
| `SUPABASE_BUCKET` | No | Supabase storage bucket name (default: `app-storage`) |
| `ALLOWED_ORIGINS` | No | Comma-separated CORS allowed origins |

*At least Google Cloud Vertex AI configuration or OpenAI API Key must be set for image generation. Application Default Credentials (ADC) must be configured on the host machine/service.

---

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) before submitting a pull request.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## 🔒 Security

For security vulnerabilities, please refer to our [Security Policy](SECURITY.md).

---

<div align="center">

**Built with ❤️ by [Shubham Gadhiya](https://www.linkedin.com/in/shubham-gadhiya/) — [SG Enterprise](https://github.com/Shubham30522)**

</div>
