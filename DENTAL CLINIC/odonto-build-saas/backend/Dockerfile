# USAMOS UNA IMAGEN SLIM (Menor superficie de ataque - OWASP)
FROM python:3.11-slim

# EVITAMOS ARCHIVOS PYC (Limpieza)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# INSTALAMOS DEPENDENCIAS DEL SISTEMA (Necesarias para compilar)
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# COPIAMOS REQUIREMENTS E INSTALAMOS
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --- SEGURIDAD AVANZADA (Ley 21.663) ---
# Creamos un usuario no-root para ejecutar la aplicación
RUN useradd -m -u 1000 odonto_user

# Copiamos el código
COPY . .

# Cambiamos el dueño de los archivos al usuario seguro
RUN chown -R odonto_user:odonto_user /app

# Cambiamos al usuario seguro (Dejamos de ser root aquí)
USER odonto_user

# EXPOSICIÓN DE PUERTO
EXPOSE 8000

# COMANDO DE INICIO
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]