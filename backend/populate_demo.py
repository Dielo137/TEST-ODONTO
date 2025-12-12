import models, database, security
from sqlalchemy.orm import Session
from datetime import datetime
import uuid

# ==========================================
# 🕒 AJUSTE DE HORA PARA VIDEO (UTC vs CHILE)
# ==========================================
# En Chile somos UTC-3 (Verano). 
# Si guardamos a las 12:00 UTC -> Se verá a las 09:00 AM en el Dashboard
# Si guardamos a las 14:00 UTC -> Se verá a las 11:00 AM en el Dashboard

# Cita Conflicto (Martes 16)
CITA_LUNES_9AM_START = datetime(2025, 12, 16, 12, 0, 0) 
CITA_LUNES_9AM_END = datetime(2025, 12, 16, 13, 0, 0)

# Cita Relleno (Viernes 19)
CITA_JUEVES_11AM_START = datetime(2025, 12, 19, 14, 0, 0)
CITA_JUEVES_11AM_END = datetime(2025, 12, 19, 15, 0, 0)

def create_data():
    db = database.SessionLocal()

    # ==========================================
    # 🧹 FASE 0: LIMPIEZA TOTAL (NUCLEAR)
    # ==========================================
    print("🧹 Iniciando limpieza de base de datos...")
    try:
        # Borramos en orden inverso para respetar las claves foráneas
        db.query(models.AuditLog).delete()
        db.query(models.Appointment).delete()
        db.query(models.Patient).delete()
        # WebsiteConfig depende de Clinic, User depende de Clinic
        db.query(models.WebsiteConfig).delete() 
        db.query(models.User).delete()
        db.query(models.Clinic).delete()
        
        db.commit()
        print("✨ Base de datos 100% limpia. Eliminando datos antiguos.")
    except Exception as e:
        db.rollback()
        print(f"⚠️ Advertencia durante limpieza: {e}")
        # Si falla la limpieza, intentamos seguir igual, pero probablemente fallará abajo.

    # ==========================================
    # 🏗️ FASE 1: CREACIÓN DE DATOS
    # ==========================================
    
    # 1. Crear Clínicas
    print("🏥 Creando Clínicas...")
    clinic_azul = models.Clinic(
        name="Clínica Sonrisa Perfecta", 
        rut="76.111.111-1", 
        address="Av. Providencia 1234, Santiago", 
        phone="+56 2 2333 4444",
        domain="sonrisa-perfecta.cl"
    )
    clinic_verde = models.Clinic(
        name="Clínica Dental Sur", 
        rut="76.222.222-2", 
        address="Calle Los Robles 456, Valdivia", 
        phone="+56 63 2444 5555",
        domain="dental-sur.cl"
    )
    db.add(clinic_azul)
    db.add(clinic_verde)
    db.commit() # Commit para obtener IDs reales

    # 2. Configuraciones Web
    print("🌐 Configurando Sitios Web...")
    config_azul = models.WebsiteConfig(
        domain="sonrisa-perfecta.cl",
        primary_color="#1E3A8A", # Azul
        welcome_text="Expertos en tu mejor sonrisa.",
        clinic_id=clinic_azul.id
    )
    config_verde = models.WebsiteConfig(
        domain="dental-sur.cl",
        primary_color="#10B981", # Verde
        welcome_text="Odontología cercana y natural.",
        clinic_id=clinic_verde.id
    )
    db.add(config_azul)
    db.add(config_verde)

    # 3. Usuarios
    print("👨‍⚕️ Contratando Personal...")
    admin_user = models.User(
        email="admin@dental.cl",
        hashed_password=security.get_password_hash("OdontoSecurePass2025"),
        full_name="Administrador General",
        role="ADMIN",
        clinic_id=clinic_azul.id
    )
    
    dr_house = models.User(
        email="house@dental.cl",
        hashed_password=security.get_password_hash("vicodin"),
        full_name="Dr. Gregory House",
        role="DENTIST",
        clinic_id=clinic_azul.id
    )
    db.add(admin_user)
    db.add(dr_house)
    db.commit()

    # 4. Pacientes
    print("👤 Registrando Pacientes...")
    paciente_wilson = models.Patient(
        full_name="James Wilson",
        rut="11.111.111-1",
        email="wilson@hospital.com",
        clinic_id=clinic_azul.id
    )
    paciente_cuddy = models.Patient(
        full_name="Lisa Cuddy",
        rut="22.222.222-2",
        email="cuddy@hospital.com",
        clinic_id=clinic_azul.id
    )
    db.add(paciente_wilson)
    db.add(paciente_cuddy)
    db.commit()

    # 5. Citas
    print("📅 Agendando Citas...")
    
    # Cita 1: Conflicto (Martes 09:00 AM Chile)
    cita1 = models.Appointment(
        start_time=CITA_LUNES_9AM_START,
        end_time=CITA_LUNES_9AM_END,
        status="CONFIRMED",
        patient_name="James Wilson",
        patient_rut="11.111.111-1",
        doctor_id=dr_house.id,
        clinic_id=clinic_azul.id,
        patient_id=paciente_wilson.id
    )

    # Cita 2: Relleno (Viernes 11:00 AM Chile)
    cita2 = models.Appointment(
        start_time=CITA_JUEVES_11AM_START,
        end_time=CITA_JUEVES_11AM_END,
        status="CONFIRMED",
        patient_name="Lisa Cuddy",
        patient_rut="22.222.222-2",
        doctor_id=dr_house.id,
        clinic_id=clinic_azul.id,
        patient_id=paciente_cuddy.id
    )
    db.add(cita1)
    db.add(cita2)
    db.commit()

    print("✅ ¡DATOS CARGADOS Y HORA AJUSTADA! Listo para grabar.")
    db.close()

if __name__ == "__main__":
    create_data()