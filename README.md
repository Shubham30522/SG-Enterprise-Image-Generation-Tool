<div align="center">

# 🖼️ Gemini Auto Tool

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

Gemini Auto Tool is an AI-driven automation platform built by **SG Enterprise** that eliminates the need for expensive physical photoshoots. It takes a single raw product photo and generates consistent, multi-angle catalogue images (front, back, side, neck, detail, waistband, hem) using advanced generative AI models.

### The Problem

Independent sellers on platforms like **Meesho** and **Flipkart** spend ₹2,000–₹10,000 per product on professional photoshoots. This cost barrier prevents catalogue scaling and directly impacts revenue potential.

### Our Solution

By leveraging **Google Gemini Pro Vision** and **OpenAI GPT Image 2**, we reduce cataloguing costs by **up to 90%** and compress time-to-market from **days to minutes**.

---

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| 🤖 **Multi-Provider AI** | Seamless switching between Google Gemini and OpenAI GPT Image 2 |
| 📸 **Multi-Angle Generation** | Auto-generates front, back, side, neck, detail, and custom views |
| ⚡ **Real-Time Streaming** | Server-Sent Events (SSE) for live generation progress |
| 🎨 **Smart Prompt Engineering** | Auto-analyzes reference images to generate optimal prompts |
| 🔧 **Product Management** | Full CRUD operations for products, SKUs, and prompt templates |
| 🌐 **Cloud Storage** | Supabase integration for persistent image storage |
| 🤖 **Platform Automation** | Selenium-driven workflows for Meesho catalogue publishing |
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
│                  STORAGE & AUTOMATION                         │
│                                                              │
│   ┌──────────────┐  ┌────────────┐  ┌──────────────────────┐ │
│   │  Supabase    │  │  Local FS  │  │ Selenium Automation  │ │
│   │  (Cloud)     │  │  (Dev)     │  │ (Meesho Publishing)  │ │
│   └──────────────┘  └────────────┘  └──────────────────────┘ │
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
| **Automation** | Selenium WebDriver | E-commerce platform publishing |
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
GOOGLE_API_KEY=your_gemini_api_key
OPENAI_API_KEY=your_openai_api_key        # Optional
DEFAULT_AI_PROVIDER="gemini"               # or "chatgpt"
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
├── main.py                # Desktop GUI (Tkinter) — legacy interface
├── web_app.py             # Streamlit UI — standalone web interface
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
├── automation/            # Browser automation layer
│   ├── script_executor.py # Selenium JSON script runner
│   └── scripts/           # Automation flow definitions
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
| `GET` | `/api/products` | List all available products |
| `GET` | `/api/products/{product}/skus` | List SKUs for a product |
| `POST` | `/api/generate` | Start image generation job |
| `GET` | `/api/jobs/{job_id}/stream` | SSE stream for job progress |
| `GET` | `/api/jobs/{job_id}/status` | Poll job status |
| `POST` | `/api/products` | Create a new product |
| `DELETE` | `/api/products/{product}` | Delete a product |
| `POST` | `/api/upload-reference` | Upload reference image |
| `POST` | `/api/auto-tune` | Auto-generate prompts from reference |

---

## 🚢 Deployment

### Frontend (Vercel)

The React frontend is deployed on Vercel with automatic deployments from the `master` branch.

```bash
# Build for production
cd web && npm run build
```

### Backend (Render)

The FastAPI backend runs on Render with the following environment variables:

| Variable | Required | Description |
|----------|----------|-------------|
| `GOOGLE_API_KEY` | Yes* | Google Gemini API key |
| `OPENAI_API_KEY` | No | OpenAI API key |
| `DEFAULT_AI_PROVIDER` | No | Default: `gemini` |
| `SUPABASE_URL` | Yes | Supabase project URL |
| `SUPABASE_KEY` | Yes | Supabase anon key |
| `CORS_ORIGINS` | No | Comma-separated allowed origins |

*At least one AI provider key is required.

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
