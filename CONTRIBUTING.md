# Contributing to Shotloom

Thank you for your interest in contributing to **Shotloom**! We welcome contributions from the community and are grateful for any help.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Commit Convention](#commit-convention)
- [Pull Request Process](#pull-request-process)

## Code of Conduct

This project adheres to the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## Getting Started

1. **Fork** the repository
2. **Clone** your fork locally
3. **Create** a feature branch from `master`
4. **Make** your changes
5. **Test** your changes locally
6. **Submit** a Pull Request

## Development Setup

### Prerequisites

- Python 3.9+
- Node.js 18+
- A valid Google Gemini API key (for testing AI features)

### Backend Setup

```bash
# Install Python dependencies
pip install -r requirements.txt

# Start the FastAPI server
uvicorn server:app --reload --port 8000
```

### Frontend Setup

```bash
cd web
npm install
npm run dev
```

The frontend dev server runs at `http://localhost:5173` and proxies API calls to `localhost:8000`.

## Coding Standards

### Python

- Follow **PEP 8** style guidelines
- Use type hints where practical
- Write descriptive docstrings for public functions
- Keep functions focused and under 50 lines where possible

### JavaScript / React

- Use functional components with hooks
- Follow the existing component structure
- Use meaningful variable and function names
- Keep components focused and reusable

### General

- Write self-documenting code
- Don't leave commented-out code in production
- Handle errors gracefully — never silently swallow exceptions

## Commit Convention

We use [Conventional Commits](https://www.conventionalcommits.org/) for clear, machine-readable commit history:

```
feat: add new feature
fix: resolve a bug
docs: update documentation
style: formatting, no logic change
refactor: code restructuring without feature change
test: add or update tests
chore: maintenance tasks (deps, config)
perf: performance improvements
```

**Examples:**
```bash
git commit -m "feat: add batch image generation support"
git commit -m "fix: resolve SSE connection timeout on Render"
git commit -m "docs: update API endpoint documentation"
```

## Pull Request Process

1. **Branch Naming**: Use descriptive branch names
   - `feature/batch-generation`
   - `fix/sse-timeout`
   - `docs/api-endpoints`

2. **PR Requirements**:
   - Clear description of changes and motivation
   - All existing tests pass
   - New features include relevant tests where applicable
   - No breaking changes without prior discussion

3. **Review Process**:
   - At least one maintainer approval required
   - Address all review feedback before merging
   - Squash merge to keep history clean

## 🙏 Thank You

Every contribution matters — whether it's fixing a typo, improving documentation, or building a major feature. Thank you for helping make Shotloom better!
