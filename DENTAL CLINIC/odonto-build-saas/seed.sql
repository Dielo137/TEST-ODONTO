-- SCRIPT DE SIEMBRA v7.0 (GOLDEN COPY CON DATOS COMPLETOS) --

-- 1. CREAR CLÍNICAS (TENANTS) - AHORA CON DIRECCIÓN Y TELÉFONO
INSERT INTO clinics (id, name, rut, address, phone) VALUES 
('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', 'Clínica Dental Sonrisa Perfecta', '76.111.222-3', 'Av. Providencia 123, Santiago', '+56212345678') ON CONFLICT (id) DO UPDATE SET address = EXCLUDED.address, phone = EXCLUDED.phone;
INSERT INTO clinics (id, name, rut, address, phone) VALUES 
('b1ffca88-8d0b-4ef8-cc7d-7cc9bd380b22', 'Odontología Integral del Sur', '78.444.555-6', 'Calle O Higgins 456, Puerto Montt', '+56652987654') ON CONFLICT (id) DO UPDATE SET address = EXCLUDED.address, phone = EXCLUDED.phone;

-- 2. CONFIGURACIÓN DE SITIOS WEB
INSERT INTO website_configs (id, clinic_id, domain, primary_color, hero_image, hero_text, welcome_text) VALUES
(gen_random_uuid(), 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', 'sonrisa-perfecta.cl', '#3B82F6', '/hero-sonrisa.jpg', 'Donde cuidamos tu salud dental con la mejor tecnología.', 'Bienvenido a Sonrisa Perfecta') ON CONFLICT (clinic_id) DO NOTHING;
INSERT INTO website_configs (id, clinic_id, domain, primary_color, hero_image, hero_text, welcome_text) VALUES
(gen_random_uuid(), 'b1ffca88-8d0b-4ef8-cc7d-7cc9bd380b22', 'dental-sur.cl', '#10B981', '/hero-sur.jpg', 'Ofrecemos un servicio cercano y familiar para toda la comunidad.', 'En Dental Sur') ON CONFLICT (clinic_id) DO NOTHING;

-- 3. CREAR USUARIOS (STAFF)
INSERT INTO users (id, email, hashed_password, full_name, role, clinic_id) VALUES
('c2ccda99-9d1c-5ff8-dd8d-8dd9cd380c33', 'admin@sonrisa-perfecta.cl', '$2b$12$7dxHSpnG/tbuorK2X4h6h.qA8ZhhrwApPKaffuNM2moib9D8TCwRS', 'Dr. James Wilson', 'DENTIST', 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11') ON CONFLICT (id) DO NOTHING;
INSERT INTO users (id, email, hashed_password, full_name, role, clinic_id) VALUES
('d3ddfa11-1e2d-6aa9-ee9e-9ee1de380d44', 'admin@dental-sur.cl', '$2b$12$7dxHSpnG/tbuorK2X4h6h.qA8ZhhrwApPKaffuNM2moib9D8TCwRS', 'Dra. Lisa Cuddy', 'DENTIST', 'b1ffca88-8d0b-4ef8-cc7d-7cc9bd380b22') ON CONFLICT (id) DO NOTHING;

-- 4. CREAR PACIENTES
INSERT INTO patients (id, full_name, rut, clinic_id) VALUES 
('e4eeaa22-2f3e-7bb1-ff1f-1ff2ef380e55', 'Juan Pérez', '12.345.678-5', 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11') ON CONFLICT (id) DO NOTHING;
INSERT INTO patients (id, full_name, rut, clinic_id) VALUES 
('f5ffbb33-3a4f-8cc2-aa2a-2aa3fa380f66', 'Ana Silva', '9.876.543-K', 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11') ON CONFLICT (id) DO NOTHING;

-- 5. CREAR CITAS INICIALES
INSERT INTO appointments (id, start_time, end_time, status, patient_name, patient_rut, doctor_id, clinic_id, patient_id) VALUES
(gen_random_uuid(), '2025-12-16 09:00:00-03', '2025-12-16 09:30:00-03', 'CONFIRMED', 'Juan Pérez', '12.345.678-5', 'c2ccda99-9d1c-5ff8-dd8d-8dd9cd380c33', 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', 'e4eeaa22-2f3e-7bb1-ff1f-1ff2ef380e55');
INSERT INTO appointments (id, start_time, end_time, status, patient_name, patient_rut, doctor_id, clinic_id, patient_id) VALUES
(gen_random_uuid(), '2025-12-18 11:00:00-03', '2025-12-18 11:30:00-03', 'CONFIRMED', 'Ana Silva', '9.876.543-K', 'c2ccda99-9d1c-5ff8-dd8d-8dd9cd380c33', 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', 'f5ffbb33-3a4f-8cc2-aa2a-2aa3fa380f66');