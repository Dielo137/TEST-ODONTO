from sqlalchemy import Column, String, Boolean, ForeignKey, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from database import Base

# --- MODELO MULTI-TENANT (Clínicas) ---
class Clinic(Base):
    __tablename__ = "clinics"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String(100), nullable=False)
    rut = Column(String(20), unique=True, index=True, nullable=False)
    address = Column(String(200))
    phone = Column(String(20))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)
    domain = Column(String(100), unique=True, index=True, nullable=True)
    
    # Relaciones (El cerebro del sistema)
    users = relationship("User", back_populates="clinic")
    website_config = relationship("WebsiteConfig", back_populates="clinic", uselist=False)
    appointments = relationship("Appointment", back_populates="clinic")
    patients = relationship("Patient", back_populates="clinic") # <--- NUEVA RELACIÓN CRÍTICA

# --- USUARIOS DEL SISTEMA (Staff) ---
class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False) # CORREGIDO: Coincide con auth.py
    full_name = Column(String(100))
    role = Column(String(20)) # ADMIN, DENTIST, RECEPTIONIST
    is_active = Column(Boolean, default=True)
    
    # FK y Relación
    clinic_id = Column(UUID(as_uuid=True), ForeignKey("clinics.id"))
    clinic = relationship("Clinic", back_populates="users")

# --- GESTIÓN DE PACIENTES (NUEVA TABLA - Requisito Eval 3) ---
class Patient(Base):
    __tablename__ = "patients"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    full_name = Column(String(100), nullable=False)
    rut = Column(String(20), index=True, nullable=False) # RUT Chileno
    email = Column(String(100))
    phone = Column(String(20))
    address = Column(String(200))
    
    # Auditoría de creación
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)

    # Multi-tenancy (Ley 19.628: Aislamiento de Datos)
    clinic_id = Column(UUID(as_uuid=True), ForeignKey("clinics.id"))
    clinic = relationship("Clinic", back_populates="patients")
    
    # Relación con sus citas
    appointments = relationship("Appointment", back_populates="patient_rel")

# --- CONSTRUCTOR WEB (DIWY) ---
class WebsiteConfig(Base):
    __tablename__ = "website_configs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    domain = Column(String(100), unique=True)
    primary_color = Column(String(7), default="#1E3A8A") # Color azul por defecto
    config_json = Column(JSONB, default={}) # Estructura flexible para el CMS
    logo_url = Column(String(255))
    welcome_text = Column(Text)
    hero_image = Column(String(255), nullable=True) # Para la URL de la imagen de cabecera
    hero_text = Column(Text, nullable=True)         # Para el texto grande de bienvenida

    
    clinic_id = Column(UUID(as_uuid=True), ForeignKey("clinics.id"), unique=True)
    clinic = relationship("Clinic", back_populates="website_config")

# --- CITAS (CORE DEL NEGOCIO) ---
class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=False)
    status = Column(String(20), default="PENDING") 
    
    # Snapshot Data (Datos congelados al momento de la reserva)
    patient_name = Column(String(100))
    patient_rut = Column(String(20))
    
    # Relaciones Fuertes (Integridad Referencial)
    clinic_id = Column(UUID(as_uuid=True), ForeignKey("clinics.id"))
    clinic = relationship("Clinic", back_populates="appointments")
    
    # Relación con el Doctor (User)
    doctor_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    doctor = relationship("User")

    # Relación con el Paciente (Tabla Patient)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.id"), nullable=True)
    patient_rel = relationship("Patient", back_populates="appointments")

# --- AUDITORÍA Y SEGURIDAD (LEY 20.584) ---
class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    action = Column(String(50), nullable=False) 
    details = Column(String) 
    ip_address = Column(String(50))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    clinic_id = Column(UUID(as_uuid=True), ForeignKey("clinics.id"), nullable=True)