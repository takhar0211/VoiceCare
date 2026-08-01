import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

from routers import audio, patients, visits, rag, prescription, analytics, patient_memory, patient_portal, auth

app = FastAPI(
    title="VoiceCare API",
    description="AI-powered clinical documentation system for Indian hospitals",
    version="1.0.0",
)

# CORS middleware
FRONTEND_URL = os.environ.get("FRONTEND_URL", "")

# Default allowed origins
cors_origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:3000",
    "https://voice-care-37i7.vercel.app",
]

if FRONTEND_URL:
    cors_origins.extend([u.strip().rstrip("/") for u in FRONTEND_URL.split(",") if u.strip()])

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Register routers
app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(audio.router, prefix="/api/audio", tags=["Audio"])
app.include_router(patients.router, prefix="/api/patients", tags=["Patients"])
app.include_router(visits.router, prefix="/api/visits", tags=["Visits"])
app.include_router(rag.router, prefix="/api/rag", tags=["RAG"])
app.include_router(prescription.router, prefix="/api/prescription", tags=["Prescription"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["Analytics"])
app.include_router(patient_memory.router, prefix="/api/memory", tags=["Patient Memory"])
app.include_router(patient_portal.router, prefix="/api/portal", tags=["Patient Portal"])


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "voicecare"}

@app.get("/cors-debug")
async def cors_debug():
    return {
        "frontend_url": FRONTEND_URL,
        "cors_origins": cors_origins,
    }
    
@app.get("/")
async def root():
    return {
        "message": "VoiceCare API",
        "docs": "/docs",
        "health": "/health",
    }

@app.get("/debug")
async def debug():
    """Temporary debug endpoint to check what's failing."""
    checks = {}
    
    # Check JWT import
    try:
        import jwt
        checks["jwt_import"] = f"OK (version: {getattr(jwt, '__version__', 'unknown')})"
    except Exception as e:
        checks["jwt_import"] = f"FAIL: {e}"
    
    # Check bcrypt import
    try:
        import bcrypt
        checks["bcrypt_import"] = "OK"
    except Exception as e:
        checks["bcrypt_import"] = f"FAIL: {e}"
    
    # Check supabase connection
    try:
        from db.supabase_client import get_supabase
        db = get_supabase()
        result = db.table("users").select("id").limit(1).execute()
        checks["supabase"] = f"OK (connected, users table accessible)"
    except Exception as e:
        checks["supabase"] = f"FAIL: {e}"
    
    # Check env vars
    checks["env_jwt_secret"] = "SET" if os.environ.get("JWT_SECRET") else "NOT SET (using default)"
    checks["env_supabase_url"] = "SET" if os.environ.get("SUPABASE_URL") else "NOT SET"
    checks["env_supabase_key"] = "SET" if os.environ.get("SUPABASE_SERVICE_KEY") else "NOT SET"
    
    return checks
