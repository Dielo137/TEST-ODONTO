# 🦷 OdontoBuild SaaS - Backend API v1.0

![Status](https://img.shields.io/badge/Status-Backend_Production_Ready-green)
![Design](https://img.shields.io/badge/Design-Security_&_Privacy_by_Design-blue)
![Security](https://img.shields.io/badge/Security-OWASP_API_Top_10-red)
![Tech](https://img.shields.io/badge/Tech-FastAPI_Docker_PostgreSQL-orange)

**Sistema Operativo Digital para Clínicas Dentales.**
Plataforma SaaS Vertical diseñada para cerrar la brecha de digitalización de las PYMEs odontológicas en Chile, con un enfoque estricto en **Seguridad por Diseño**, **Privacidad por Defecto** y cumplimiento de la normativa de salud.

---

## 📚 Ingeniería y Arquitectura (Documentación Visual)

La ingeniería del sistema se encuentra detallada en la carpeta [`/docs`](./docs). Estos artefactos definen la estructura lógica, física y de negocio del proyecto:

- **[01_arquitectura_cloud_aws.png](./docs/01_arquitectura_cloud_aws.png):** Diseño de infraestructura segura en AWS (VPC, WAF, RDS).
- **[02_flujo_trabajo_gitflow.png](./docs/02_flujo_trabajo_gitflow.png):** Estrategia de ramificación y CI/CD.
- **[03_diagrama_casos_uso.png](./docs/03_diagrama_casos_uso.png):** Actores y alcance funcional del sistema.
- **[04_proceso_negocio_bpmn.png](./docs/04_proceso_negocio_bpmn.png):** Flujo BPMN del proceso crítico de agendamiento.
- **[05_diagrama_componentes.png](./docs/05_diagrama_componentes.png):** Arquitectura Modular del Backend (Routers, Services, ORM).
- **[06_diagrama_entidad_relacion.png](./docs/06_diagrama_entidad_relacion.png):** Modelo de Datos Multi-tenant con Trazabilidad.
- **[07_diagrama_secuencia_agendamiento.png](./docs/07_diagrama_secuencia_agendamiento.png):** Lógica transaccional ACID con bloqueo pesimista.
- **[08_contrato_api_rest.png](./docs/08_contrato_api_rest.png):** Especificación de interfaces (OpenAPI/Swagger).

---

## 🛡️ Auditoría de Cumplimiento Normativo (Chile 2025)

Este software ha sido auditado para cumplir y/o prepararse para la siguiente legislación:

### 1. Ciberseguridad y Delitos Informáticos (Ley 21.663 & 21.668)
*   **Gestión de Vulnerabilidades:** Uso de imagen Docker `slim`, usuario no-root (`odonto_user`) y dependencias fijadas para minimizar superficie de ataque y prevenir Supply Chain Attacks.
*   **Prevención de Acceso Ilícito:** Autenticación robusta con JWT y hashing de contraseñas con Bcrypt.

### 2. Protección de Datos (Ley 19.628 & Nueva Ley 21.719)
*   **Aislamiento Lógico (Multi-tenancy):** Los datos están aislados por `clinic_id` en cada consulta SQL, mitigando la vulnerabilidad #1 de OWASP API (BOLA).
*   **Calidad del Dato:** Validación algorítmica del RUT Chileno (Módulo 11) en la capa de validación (Schemas).

### 3. Normativa de Salud (Ley 20.584 & 21.746)
*   **Trazabilidad (Art. 13, Ley 20.584):** Módulo `AuditLog` inmutable que registra la creación de pacientes y citas.
*   **Preparación para Interoperabilidad (Ley 21.746):** Uso de estándares de datos (UUID, ISO 8601) para facilitar la futura integración con sistemas de Ficha Clínica Electrónica Única (HL7 FHIR).

---

## 🚀 Despliegue Seguro y Verificación (Local)

### Prerrequisitos
- Docker Desktop (Running) & Git

### Instalación
1.  **Clonar y configurar:**
    ```bash
    git clone <URL_REPO> && cd odonto-build-saas
    cp .env.example .env
    ```
2.  **Desplegar:**
    ```bash
    docker-compose up --build
    ```
    *El sistema levantará PostgreSQL y FastAPI en `http://localhost:8000`.*

3.  **Primer Uso (Crear Clínica):**
    *La API requiere al menos una clínica para operar. Ejecute este SQL en la base de datos para crear una clínica de prueba:*
    ```sql
    -- Conectarse a la BD: docker-compose exec db psql -U odonto_admin -d odonto_saas
    INSERT INTO clinics (id, name, rut) VALUES (gen_random_uuid(), 'Clínica Demo', '76.123.456-7');
    ```

### 🧪 Protocolo de Pruebas (Smoke Test)
Acceda a `http://localhost:8000/docs` y siga este flujo:

1.  **Registro:** `POST /auth/register` (Usando el `clinic_id` generado en el paso anterior).
2.  **Login:** `POST /auth/login` (Obtener JWT).
3.  **Autorización:** Botón "Authorize" -> `Bearer <TOKEN>`.
4.  **Crear Paciente:** `POST /patients/`.
5.  **Crear Cita:** `POST /appointments/`.
6.  **Prueba de Concurrencia:** Ejecute de nuevo el `POST /appointments/` -> **Debe recibir Error 409 Conflict**.

---
*Desarrollado para Proyecto Integrado - Ingeniería en Informática 2025*
*Copyright (c) 2025 - OdontoBuild SpA - Todos los derechos reservados.*