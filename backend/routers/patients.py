from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import json
import models, database, schemas, security

router = APIRouter(prefix="/patients", tags=["Gestión de Pacientes"])

@router.post("/", response_model=schemas.PatientResponse, status_code=status.HTTP_201_CREATED)
def create_patient(
    patient: schemas.PatientCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    """
    Registra un nuevo paciente en la clínica del usuario actual.
    Cumplimiento: Ley 20.584 (Trazabilidad) y OWASP BOLA.
    """
    # 1. Validación de Negocio: Evitar RUT duplicado EN ESTA clínica
    existing_patient = db.query(models.Patient).filter(
        models.Patient.rut == patient.rut,
        models.Patient.clinic_id == current_user.clinic_id
    ).first()
    
    if existing_patient:
        raise HTTPException(
            status_code=400, 
            detail=f"El paciente con RUT {patient.rut} ya existe en su clínica."
        )

    # 2. Creación del Paciente (Aislamiento Multi-tenant)
    new_patient = models.Patient(
        **patient.model_dump(),
        clinic_id=current_user.clinic_id 
    )
    db.add(new_patient)
    
    # 3. Auditoría Forense (Ley 20.584 - Trazabilidad)
    # Registramos QUIÉN creó el paciente y CUÁNDO.
    audit_log = models.AuditLog(
        action="CREATE_PATIENT",
        user_id=current_user.id,
        clinic_id=current_user.clinic_id,
        details=json.dumps({"rut": patient.rut, "name": patient.full_name}),
        ip_address="REQUEST_IP" 
    )
    db.add(audit_log)

    # 4. Commit Atómico
    try:
        db.commit()
        db.refresh(new_patient)
        return new_patient
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error al registrar paciente")

@router.get("/", response_model=List[schemas.PatientResponse])
def get_patients(
    skip: int = 0, 
    limit: int = 100,
    search: str = None,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    """
    Obtiene la lista de pacientes.
    Seguridad: Solo devuelve pacientes de la clínica del usuario (BOLA Protection).
    """
    query = db.query(models.Patient).filter(
        models.Patient.clinic_id == current_user.clinic_id,
        models.Patient.is_active == True
    )

    # Filtro de búsqueda simple (por nombre o RUT)
    if search:
        query = query.filter(
            (models.Patient.full_name.ilike(f"%{search}%")) | 
            (models.Patient.rut.ilike(f"%{search}%"))
        )

    return query.offset(skip).limit(limit).all()