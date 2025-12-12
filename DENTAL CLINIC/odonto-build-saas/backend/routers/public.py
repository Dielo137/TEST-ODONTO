from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
import database, models, schemas

router = APIRouter(
    prefix="/public", 
    tags=["Sitio Público (Generador)"]
)

@router.get("/sites/{domain}", response_model=schemas.PublicSiteData)
def get_public_site_data(domain: str, db: Session = Depends(database.get_db)):
    """
    Este endpoint es el corazón del generador de sitios.
    Es PÚBLICO y devuelve toda la data necesaria para renderizar
    el sitio web de un cliente específico.
    """
    # === CORRECCIÓN CRÍTICA INICIA AQUÍ ===

    # 1. Buscamos primero en la tabla correcta: website_configs
    website_config = db.query(models.WebsiteConfig).filter(models.WebsiteConfig.domain == domain).first()

    if not website_config:
        raise HTTPException(status_code=404, detail="Sitio no encontrado")

    # 2. Una vez encontrada la configuración, obtenemos la clínica asociada
    #    usando la relación que ya definimos en models.py.
    #    Usamos 'options' para cargar las relaciones de 'users' de forma eficiente.
    clinic = db.query(models.Clinic).options(
        joinedload(models.Clinic.users)
    ).filter(models.Clinic.id == website_config.clinic_id).first()

    if not clinic:
        # Este error es improbable si la base de datos es consistente, pero es una buena práctica de seguridad
        raise HTTPException(status_code=500, detail="Inconsistencia de datos: Configuración de sitio sin clínica asociada.")

    # === CORRECCIÓN CRÍTICA TERMINA AQUÍ ===


    # Filtramos para obtener solo los doctores
    doctors_list = [user for user in clinic.users if user.role == 'DENTIST']

    # Construimos la respuesta
    # Nota: ahora usamos 'website_config' para el config, y 'clinic' para el resto
    response_data = schemas.PublicSiteData(
        clinic_name=clinic.name,
        address=clinic.address,
        phone=clinic.phone,
        config=website_config, # Usamos el objeto que encontramos
        doctors=doctors_list
    )
    
    return response_data