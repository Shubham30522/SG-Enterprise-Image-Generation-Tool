# Security Policy

## Supported Versions

| Version | Supported          |
|---------|--------------------|
| 1.x     | ✅ Active support  |
| < 1.0   | ❌ No longer supported |

## Reporting a Vulnerability

We take security seriously at SG Enterprise. If you discover a security vulnerability in Gemini Auto Tool, please report it responsibly.

### How to Report

1. **Do NOT** open a public GitHub issue for security vulnerabilities
2. Email your findings to the maintainers with the subject line: `[SECURITY] Vulnerability Report — Gemini Auto Tool`
3. Include as much detail as possible:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

### What to Expect

- **Acknowledgment**: We will acknowledge receipt of your report within **48 hours**
- **Assessment**: We will assess the vulnerability and determine its severity within **5 business days**
- **Resolution**: Critical vulnerabilities will be patched within **7 days**; others within **30 days**
- **Disclosure**: We will coordinate with you on public disclosure timing

### Scope

The following are in scope:
- The Gemini Auto Tool application (backend + frontend)
- API endpoints exposed by `server.py`
- Authentication and authorization mechanisms
- Data handling and storage

The following are out of scope:
- Third-party services (Supabase, Vercel, Render)
- Google Gemini API or OpenAI API
- Issues in dependencies (report these to the respective maintainers)

## Security Best Practices

This project follows these security practices:
- API keys are stored in environment variables, never committed to source code
- `.env` files are excluded from version control via `.gitignore`
- CORS is configured to allow only specific origins
- User inputs are validated before processing
- Dependencies are regularly audited for known vulnerabilities
