from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import json
import models, database, schemas, security

router = APIRouter(prefix="/appointments", tags=["Agenda y Citas"])

@router.post("/", response_model=schemas.AppointmentResponse, status_code=201)
def create_appointment(
    appointment: schemas.AppointmentCreate,
    current_user: models.User = Depends(security.get_current_user),
    db: Session = Depends(database.get_db)
):
    # 1. Seguridad: Verificar que el doctor pertenezca a la misma clínica
    doctor = db.query(models.User).filter(models.User.id == appointment.doctor_id).first()
    if not doctor or doctor.clinic_id != current_user.clinic_id:
        raise HTTPException(status_code=404, detail="Doctor no encontrado o de otra clínica")

    # 2. Lógica de Negocio: Bloqueo de Horario (Prevención de Solapamiento)
    collision = db.query(models.Appointment).filter(
        models.Appointment.doctor_id == appointment.doctor_id,
        models.Appointment.status != "CANCELLED",
        models.Appointment.start_time < appointment.end_time,
        models.Appointment.end_time > appointment.start_time
    ).with_for_update().first() # SELECT FOR UPDATE (Bloqueo Pesimista DB)

    if collision:
        raise HTTPException(status_code=409, detail="Conflicto: El bloque horario ya está ocupado")

    # 3. Gestión de Datos del Paciente (Híbrido Snapshot/Relacional)
    # Si viene un patient_id, usamos ese. Si no, usamos los datos de texto (para demo rápida)
    patient_id_ref = appointment.patient_id
    
    # 4. Crear Cita
    new_appointment = models.Appointment(
        start_time=appointment.start_time,
        end_time=appointment.end_time,
        status="CONFIRMED",
        # Datos Snapshot
        patient_name=appointment.patient_name,
        patient_rut=appointment.patient_rut,
        patient_id=patient_id_ref,
        # Relaciones
        doctor_id=appointment.doctor_id,
        clinic_id=current_user.clinic_id 
    )
    db.add(new_appointment)
    
    # 5. Auditoría (Ley 20.584)
    audit_log = models.AuditLog(
        action="CREATE_APPOINTMENT",
        user_id=current_user.id,
        clinic_id=current_user.clinic_id,
        details=json.dumps({
            "doctor_id": str(appointment.doctor_id),
            "time": str(appointment.start_time),
            "patient_rut": appointment.patient_rut
        }),
        ip_address="REQUEST_IP"
    )
    db.add(audit_log)

    db.commit()
    db.refresh(new_appointment)
    return new_appointment

@router.get("/", response_model=list[schemas.AppointmentResponse])
def get_appointments(
    current_user: models.User = Depends(security.get_current_user),
    db: Session = Depends(database.get_db)
):
    # Solo citas de MI clínica
    return db.query(models.Appointment).filter(
        models.Appointment.clinic_id == current_user.clinic_id
    ).all()