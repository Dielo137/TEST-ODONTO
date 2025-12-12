from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# CONEXIÓN SEGURA
# Usamos variables de entorno para que las credenciales no estén "quemadas" en el código
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

if not SQLALCHEMY_DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")


ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

connect_args = {}

if ENVIRONMENT == "production":
    # BLINDAJE SSL: Obligatorio para datos de salud en tránsito
    connect_args = {
        "sslmode": "require", 
        "connect_timeout": 10
    }


# EL MOTOR (ENGINE)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args=connect_args,
    pool_pre_ping=True 
)


# LA FÁBRICA DE SESIONES
# Cada petición del usuario creará una sesión temporal
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# LA CLASE BASE
Base = declarative_base()

# DEPENDENCIA (INYECCIÓN)
# Esta función se usará en cada Endpoint para obtener la BD y cerrarla al terminar
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()