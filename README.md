# VoiceCare — AI-Powered Clinical Documentation

> AI-driven clinical documentation system for Indian hospitals. Doctors speak, VoiceCare listens — transcribing, analysing, and documenting patient visits in real time.

## Architecture

```
┌─────────────────────┐         ┌─────────────────────────┐
│   Frontend (Vite)   │  HTTPS  │   Backend (FastAPI)     │
│   React + Tailwind  │ ──────▶ │   Vercel Python Runtime │
│   Vercel Static     │         │                         │
└─────────────────────┘         └────────┬────────────────┘
                                         │
                        ┌────────────────┼────────────────┐
                        ▼                ▼                ▼
                   ┌─────────┐    ┌───────────┐    ┌──────────┐
                   │ Supabase│    │ Gemini /  │    │ Sarvam   │
                   │ (DB)    │    │ Groq (LLM)│    │ (ASR)    │
                   └─────────┘    └───────────┘    └──────────┘
```

## Features

- 🎙️ **Voice-to-Documentation** — Sarvam AI speech-to-text for Hindi/English clinical conversations
- 🧠 **AI Clinical Analysis** — Gemini + Groq-powered extraction of symptoms, diagnoses, prescriptions
- 📋 **Prescription Generation** — Auto-generated PDF prescriptions from visit data
- 👨‍⚕️ **Doctor Dashboard** — Patient management, visit history, analytics
- 🏥 **Patient Portal** — Health passport, medications, vitals, appointment reminders
- 🚨 **Emergency QR** — Shareable emergency health profile via QR code
- 📊 **Analytics** — Patient demographics, visit trends, diagnosis distribution

---

## Local Development

### Prerequisites

- **Node.js** ≥ 18
- **Python** ≥ 3.11
- **Supabase** project (free tier works)
- API keys for: **Gemini**, **Groq**, **Sarvam AI**

### 1. Clone & Setup

```bash
git clone <repo-url>
cd partex-ai-hackathon-main
```

### 2. Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate   # macOS/Linux
# venv\Scripts\activate    # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys

# Run
uvicorn main:app --reload --port 8000
```

### 3. Frontend

```bash
cd frontend

# Install dependencies
npm install

# Configure environment
cp .env.example .env
# Edit .env — for local dev, use: VITE_API_URL=http://localhost:8000

# Run
npm run dev
```

Open http://localhost:5173 in your browser.

### 4. Database

Run the SQL migrations in your Supabase SQL Editor in this order:

1. `supabase/schema.sql` — Core tables (patients, visits)
2. `supabase/auth_schema.sql` — Authentication tables
3. `supabase/patient_dashboard_schema.sql` — Patient portal tables

Or run `supabase/run_all_migrations.sql` to execute everything at once.

---

## Deployment (Vercel)

This project deploys as **two separate Vercel projects** — one for the backend, one for the frontend.

### Backend Deployment

1. **Create a new Vercel project** and set the **Root Directory** to `backend`
2. Vercel auto-detects the Python runtime via `vercel.json`
3. Add environment variables in **Settings → Environment Variables**:

   | Variable | Description |
   |----------|-------------|
   | `SUPABASE_URL` | Your Supabase project URL |
   | `SUPABASE_SERVICE_KEY` | Supabase service role key |
   | `SARVAM_API_KEY` | Sarvam AI API key |
   | `GEMINI_API_KEY` | Google Gemini API key |
   | `GROQ_API_KEY` | Groq API key |
   | `FRONTEND_URL` | Deployed frontend URL (for CORS) |

4. Deploy!

### Frontend Deployment

1. **Create a new Vercel project** and set the **Root Directory** to `frontend`
2. Vercel auto-detects Vite. Build settings:
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist`
3. Add environment variables:

   | Variable | Description |
   |----------|-------------|
   | `VITE_API_URL` | Deployed backend URL (e.g. `https://voicecare-api.vercel.app`) |

4. Deploy!

### Post-Deployment

After both projects are live:

1. Copy the **frontend URL** → set as `FRONTEND_URL` in the backend project
2. Copy the **backend URL** → set as `VITE_API_URL` in the frontend project
3. Redeploy both projects to pick up the new env vars

---

## Environment Variables Reference

### Backend (`backend/.env`)

| Variable | Required | Description |
|----------|----------|-------------|
| `SUPABASE_URL` | ✅ | Supabase project URL |
| `SUPABASE_SERVICE_KEY` | ✅ | Supabase service role key (not anon key) |
| `SARVAM_API_KEY` | ✅ | Sarvam AI speech-to-text API key |
| `GEMINI_API_KEY` | ✅ | Google Gemini API key |
| `GROQ_API_KEY` | ✅ | Groq API key |
| `FRONTEND_URL` | ✅ | Frontend origin for CORS (comma-separated for multiple) |

### Frontend (`frontend/.env`)

| Variable | Required | Description |
|----------|----------|-------------|
| `VITE_API_URL` | ✅ | Backend API base URL |

---

## Project Structure

```
├── backend/              # FastAPI backend
│   ├── main.py           # App entry point
│   ├── routers/          # API route handlers
│   ├── services/         # AI service integrations (Gemini, Groq, Sarvam)
│   ├── models/           # Pydantic schemas
│   ├── db/               # Supabase client
│   ├── requirements.txt  # Python dependencies
│   └── vercel.json       # Vercel deployment config
├── frontend/             # Vite + React frontend
│   ├── src/
│   │   ├── pages/        # Doctor dashboard pages
│   │   ├── patient/      # Patient portal pages & components
│   │   ├── components/   # Shared components
│   │   └── auth/         # Authentication context & guards
│   ├── package.json
│   └── vercel.json       # SPA rewrite rules
└── supabase/             # Database migrations
```

## License

MIT