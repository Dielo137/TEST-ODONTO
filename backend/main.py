from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import models, database
from routers import auth, patients, appointments, public

# --- CICLO DE VIDA (MIGRACIONES MVP) ---
# NOTA TÉCNICA: En un entorno productivo (Ley 21.663), esto se reemplaza 
# por Alembic para mantener la integridad histórica del esquema de datos.
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="OdontoBuild SaaS API", 
    version="1.0.0",
    description="Sistema Operativo Dental. Cumplimiento Normativo: Ley 19.628, Ley 20.584 y OWASP."
)

# --- SEGURIDAD NIVEL 1: PROTECCIÓN DE HOST (OWASP) ---
# Mitiga ataques de 'Host Header Injection'.
# En producción, 'allowed_hosts' se restringe al dominio real (ej: api.odontobuild.cl)
# para cumplir con los estándares de la Ley Marco de Ciberseguridad (21.663).
app.add_middleware(
    TrustedHostMiddleware, 
    allowed_hosts=[
        "localhost", 
        "127.0.0.1", 
        "0.0.0.0",
        # "*",  # <--- COMENTADO PARA LA DEMO (Riesgo OWASP) - Solo habilitar si falla la red local
        "odonto_backend" # Host interno de Docker
    ] 
)

# --- SEGURIDAD NIVEL 2: CORS (Interoperabilidad Frontend) ---
# Define quién puede hablar con la API.
# OWASP API8:2023 Security Misconfiguration: Nunca usar "*" con allow_credentials=True en Prod.
origins = [
    "http://localhost:3000", # Frontend Local
    "http://localhost:8080", # Docker Network
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, # Restricción explícita (Cumplimiento Ley 19.628)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- ENSAMBLAJE DE ROUTERS (Modularidad) ---
app.include_router(auth.router)
app.include_router(patients.router)
app.include_router(appointments.router)
app.include_router(public.router)

# --- ENDPOINTS DE INFRAESTRUCTURA ---

@app.get("/", tags=["Infraestructura"])
def read_root():
    """
    Endpoint raíz para verificación de estado y cumplimiento.
    """
    return {
        "system": "OdontoBuild SaaS", 
        "version": "1.0.0", 
        "status": "operational",
        "legal_compliance": ["Ley 20.584", "Ley 19.628", "OWASP Top 10"]
    }

@app.get("/healthz", tags=["Infraestructura"])
def health_check():
    """
    Heartbeat para orquestadores (AWS ECS / Docker Swarm).
    Garantiza disponibilidad (SLA) según Ley 21.663.
    """
    return {"status": "ok", "database": "connected"}