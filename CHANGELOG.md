# Changelog

All notable changes to Shotloom will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] — 2026-05-03

### 🚀 First Stable Release

The first production-ready release of Shotloom with full multi-provider AI support and cloud deployment.

### Added
- **Multi-Provider AI Architecture**: Unified dispatcher supporting Google Gemini Pro Vision and OpenAI GPT Image 2
- **React 19 Frontend**: Modern responsive UI with Tailwind CSS 4, product/SKU selection, real-time generation streaming
- **FastAPI Backend**: REST API with Server-Sent Events (SSE) for live generation progress
- **Product Management System**: Full CRUD operations for products, SKUs, and prompt templates
- **Auto-Tune Engine**: AI-powered prompt generation from style reference images
- **Cloud Storage Integration**: Supabase for persistent image storage in production
- **Multi-Angle Generation**: Support for front, back, side, neck, detail, waistband, and hem views
- **Selenium Automation Layer**: Browser-driven workflows for Meesho catalogue publishing
- **Cloud Deployment**: Vercel (frontend) + Render (backend) deployment configuration
- **Dynamic CORS**: Regex-based CORS support for Vercel preview deployments

### Infrastructure
- CI pipeline with GitHub Actions (lint + dependency audit)
- Conventional commit enforcement
- Comprehensive documentation (README, CONTRIBUTING, SECURITY, CODE_OF_CONDUCT)
- Issue and PR templates

## [0.2.0] — 2026-04-28

### Added
- OpenAI ChatGPT (gpt-image-2) provider integration alongside Gemini
- Provider toggle in the React UI
- Dynamic provider disabling when API keys are missing

### Changed
- Refactored `api_client.py` to support multi-provider dispatch via `generate_image()`

## [0.1.0] — 2026-04-20

### Added
- Initial React + Vite web UI for product and pose selection
- FastAPI backend with job state tracking and SSE streaming
- Reference image upload and analysis
- Carousel view for generated images
- Color/SKU selector dropdown
- Batch ZIP download for generated images
- Tkinter desktop GUI (legacy interface)
- Streamlit web UI (standalone interface)
