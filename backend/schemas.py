from pydantic import BaseModel, EmailStr, field_validator, ConfigDict, Field
from typing import Optional
from uuid import UUID
from datetime import datetime
import re 

# --- FUNCIÓN AUXILIAR DE VALIDACIÓN DE RUT (MÓDULO 11) ---
def validar_rut_chileno(rut: str) -> str:
    """
    Valida y formatea un RUT chileno usando el algoritmo Módulo 11.
    Retorna el RUT limpio y formateado (ej: 12345678-5) o lanza ValueError.
    """
    if not rut:
        raise ValueError("El RUT es obligatorio")
        
    # Limpieza: sacar puntos y guiones, pasar a mayúsculas
    rut_limpio = rut.replace(".", "").replace("-", "").upper().strip()
    
    # Regex básico para formato (números + K al final)
    if not re.match(r"^\d{1,8}[0-9K]$", rut_limpio):
        raise ValueError("Formato de RUT inválido")

    # Separar cuerpo y dígito verificador
    cuerpo = rut_limpio[:-1]
    dv_ingresado = rut_limpio[-1]

    # Algoritmo Módulo 11
    suma = 0
    multiplo = 2
    
    for c in reversed(cuerpo):
        suma += int(c) * multiplo
        multiplo += 1
        if multiplo == 8: 
            multiplo = 2
        
    resultado = 11 - (suma % 11)
    
    if resultado == 11: 
        dv_calculado = '0'
    elif resultado == 10: 
        dv_calculado = 'K'
    else: 
        dv_calculado = str(resultado)
    
    if dv_ingresado != dv_calculado:
        raise ValueError("RUT inválido (Dígito verificador incorrecto)")
    
    return f"{cuerpo}-{dv_ingresado}"


# --- ESQUEMAS DE SEGURIDAD (JWT) ---
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[str] = None
    clinic_id: Optional[str] = None


# --- ESQUEMAS DE USUARIO (STAFF) ---

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = Field(None, max_length=100)
    role: str = Field(default="RECEPTIONIST", pattern="^(ADMIN|DENTIST|RECEPTIONIST)$")

class UserCreate(UserBase):
    password: str = Field(min_length=12, max_length=50) # OWASP: Longitud mínima
    clinic_id: Optional[UUID] = None # Opcional porque al registrar la clínica se crea el primer admin

class UserResponse(UserBase):
    id: UUID
    clinic_id: UUID
    is_active: bool
    # SECURITY: Jamás devolvemos el password_hash

    model_config = ConfigDict(from_attributes=True)


# --- ESQUEMAS DE PACIENTES (NUEVO - REQUISITO CRUD) ---

class PatientBase(BaseModel):
    full_name: str = Field(min_length=3, max_length=100)
    rut: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)
    address: Optional[str] = Field(None, max_length=200)

    # Validar RUT automáticamente al recibir datos
    @field_validator('rut')
    @classmethod
    def validate_rut_field(cls, v):
        return validar_rut_chileno(v)

class PatientCreate(PatientBase):
    pass # Hereda todo, sin campos extra por ahora

class PatientResponse(PatientBase):
    id: UUID
    clinic_id: UUID
    created_at: datetime
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


# --- ESQUEMAS DE CITAS (AGENDA) ---

class AppointmentCreate(BaseModel):
    doctor_id: UUID
    start_time: datetime
    end_time: datetime
    
    # Datos "Snapshot" del paciente (para agilidad en la demo)
    patient_id: Optional[UUID] = None 
    patient_name: str
    patient_email: Optional[EmailStr] = None
    patient_rut: str

    @field_validator('patient_rut')
    @classmethod
    def validate_rut(cls, v):
        return validar_rut_chileno(v)

    @field_validator('end_time')
    @classmethod
    def validate_times(cls, v, info):
        if 'start_time' in info.data and v <= info.data['start_time']:
            raise ValueError('La hora de término debe ser posterior a la de inicio')
        return v

class AppointmentResponse(BaseModel):
    id: UUID
    start_time: datetime
    end_time: datetime
    status: str
    doctor_id: UUID
    patient_name: str
    # patient_rut se omite en la respuesta pública por privacidad, o se puede incluir si es vista interna
    
    model_config = ConfigDict(from_attributes=True)

# --- ESQUEMAS PÚBLICOS PARA EL GENERADOR DE SITIOS ---

class DoctorPublicInfo(BaseModel):
    full_name: str
    # Omitimos email, id, etc. por seguridad

    model_config = ConfigDict(from_attributes=True)

class WebsiteConfigPublic(BaseModel):
    logo_url: Optional[str] = None
    primary_color: str
    welcome_text: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class PublicSiteData(BaseModel):
    clinic_name: str
    address: Optional[str] = None
    phone: Optional[str] = None
    config: WebsiteConfigPublic
    doctors: list[DoctorPublicInfo]

    model_config = ConfigDict(from_attributes=True)