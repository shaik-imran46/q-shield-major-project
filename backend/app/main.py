from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database.database import init_db, get_all_incidents
from app.security.auth import seed_default_users
from app.api import auth, dashboard, agents, incidents, simulator, quantum, analysis
from app.simulator.normal import create_normal_event
from app.simulator.mitm import create_mitm_event
from app.simulator.replay import create_replay_event
from app.simulator.tampering import create_file_tampering_event
from app.risk.risk_engine import risk_engine
import logging

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("Q-Shield")

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Adaptive Multi-Agent Cyber-Risk Detection and Post-Quantum Security Framework - Final Year Major Project Simulation Platform",
    version=settings.VERSION
)

# Enable CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Startup Hook
@app.on_event("startup")
def on_startup():
    logger.info("Initializing Q-Shield Database and Security Registries...")
    init_db()
    seed_default_users()
    
    # Pre-seed initial incidents if database is fresh
    existing = get_all_incidents(limit=5)
    if len(existing) == 0:
        logger.info("Generating initial multi-agent baseline incidents...")
        risk_engine.process_security_event(create_normal_event())
        risk_engine.process_security_event(create_tampering_event()) if False else None
        risk_engine.process_security_event(create_replay_event())
        risk_engine.process_security_event(create_file_tampering_event())
        risk_engine.process_security_event(create_mitm_event())
        logger.info("Seed incidents created successfully.")
    logger.info("Q-Shield Framework Core is READY.")

# Include API Routers
app.include_router(auth.router, prefix=settings.API_PREFIX)
app.include_router(dashboard.router, prefix=settings.API_PREFIX)
app.include_router(agents.router, prefix=settings.API_PREFIX)
app.include_router(incidents.router, prefix=settings.API_PREFIX)
app.include_router(simulator.router, prefix=settings.API_PREFIX)
app.include_router(quantum.router, prefix=settings.API_PREFIX)
app.include_router(analysis.router, prefix=settings.API_PREFIX)

@app.get("/api/health", tags=["Health"])
def health_check():
    return {
        "status": "HEALTHY",
        "framework": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "agents_online": 5,
        "quantum_services": ["PQC (ML-KEM-768 / ML-DSA-65)", "QRNG Simulator", "BB84 QKD Simulator"],
        "disclaimer": "Academic Demonstration & Safe Simulation Platform"
    }

@app.get("/", tags=["Root"])
def root():
    return {
        "message": "Welcome to Q-Shield: Adaptive Multi-Agent Cyber-Risk Detection and Post-Quantum Security Framework",
        "docs_url": "/docs",
        "api_health": "/api/health"
    }
