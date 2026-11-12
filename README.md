# AI-Driven API Security Assessment and Vulnerability Detection System

A comprehensive, AI-powered API security assessment platform that combines conventional automated security testing with Google Gemini AI-assisted analysis to identify vulnerabilities based on the OWASP API Security Top 10.

## 🎯 Project Overview

This platform allows users to:
- Submit API URLs or upload OpenAPI/Swagger specifications
- Automatically discover and inventory API endpoints
- Generate security test cases using Google Gemini AI
- Execute controlled security assessments against authorized targets
- Identify potential vulnerabilities based on OWASP API Security Top 10:2023
- Analyze actual HTTP responses with AI assistance
- Generate professional PDF security assessment reports

## 🏗️ Technology Stack

### Frontend
- React 18 + TypeScript
- Vite
- Tailwind CSS
- React Router
- Axios
- Recharts
- Lucide React
- React Hook Form + Zod

### Backend
- Python + FastAPI
- SQLAlchemy + Alembic
- SQLite (dev) / PostgreSQL (prod)
- HTTPX
- Argon2 password hashing
- JWT authentication
- ReportLab (PDF generation)

### AI Integration
- Google Gemini API (google-genai SDK)
- Structured JSON responses
- Custom agent orchestration

## 📁 Project Structure

```
api-security-assessment/
├── frontend/          # React TypeScript application
├── backend/           # FastAPI Python application
├── demo-api/          # Deliberately vulnerable demo API
├── docs/              # Project documentation
├── docker-compose.yml # PostgreSQL setup (optional)
├── README.md          # This file
└── .gitignore
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- (Optional) Docker for PostgreSQL

### 1. Clone & Setup Backend

```bash
cd api-security-assessment/backend

# Create virtual environment
python -m venv venv

# Activate (Windows)
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Copy environment config
copy .env.example .env
# Edit .env with your settings (especially GEMINI_API_KEY)

# Run database migrations
alembic upgrade head

# Start backend
uvicorn app.main:app --reload --port 8000
```

### 2. Setup Frontend

```bash
cd api-security-assessment/frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

### 3. Start Demo API (for testing)

```bash
cd api-security-assessment/demo-api

# Install dependencies
pip install -r requirements.txt

# Start demo API
uvicorn app.main:app --port 8001 --host 127.0.0.1
```

### 4. Access the Application

- **Frontend**: http://localhost:5173
- **Backend API Docs**: http://localhost:8000/docs
- **Demo API Docs**: http://localhost:8001/docs

## 🔑 Environment Configuration

Copy `backend/.env.example` to `backend/.env` and configure:

| Variable | Description | Default |
|----------|-------------|---------|
| DATABASE_URL | Database connection string | sqlite:///./app.db |
| JWT_SECRET_KEY | Secret key for JWT tokens | (must change) |
| JWT_ALGORITHM | JWT algorithm | HS256 |
| ACCESS_TOKEN_EXPIRE_MINUTES | Token expiry | 30 |
| GEMINI_API_KEY | Google Gemini API key | (optional) |
| GEMINI_MODEL | Gemini model name | gemini-2.0-flash |
| FRONTEND_URL | Frontend URL for CORS | http://localhost:5173 |

## 🧪 Demo Accounts

The demo API includes these test accounts (**DEMONSTRATION DATA ONLY**):

| Username | Password | Role |
|----------|----------|------|
| user1 | password123 | user |
| user2 | password456 | user |
| admin | adminpass | admin |

## 🔒 Security Notice

- This tool is for authorized security testing ONLY
- Only test APIs you own or have explicit permission to test
- The demo API contains intentional vulnerabilities and must NEVER be exposed publicly
- All findings require actual evidence — no fabricated results

## 📊 OWASP API Security Top 10:2023 Coverage

| # | Category | Status |
|---|----------|--------|
| API1 | Broken Object Level Authorization | ✅ Implemented |
| API2 | Broken Authentication | ✅ Implemented |
| API3 | Broken Object Property Level Authorization | ✅ Implemented |
| API4 | Unrestricted Resource Consumption | ✅ Implemented |
| API5 | Broken Function Level Authorization | ✅ Implemented |
| API6 | Unrestricted Access to Sensitive Business Flows | ✅ Implemented |
| API7 | Server-Side Request Forgery (SSRF) | ✅ Implemented |
| API8 | Security Misconfiguration | ✅ Implemented |
| API9 | Improper Inventory Management | ✅ Implemented |
| API10 | Unsafe Consumption of APIs | ✅ Implemented |

## 📝 License

This project is developed as a Final-Year B.Tech Computer Science Engineering project.

## ⚠️ Disclaimer

This tool is for educational and authorized security testing purposes only. Users are responsible for ensuring they have proper authorization before testing any API. The developers are not responsible for any misuse of this tool.
