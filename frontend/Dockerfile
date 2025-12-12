# USAMOS NODE (Entorno de Javascript)
FROM node:18-alpine

WORKDIR /app

# Instalar dependencias
COPY package*.json ./
RUN npm install

# Copiar el código fuente
COPY . .

# Exponer el puerto donde corre Next.js
EXPOSE 3000

# Comando para iniciar en modo desarrollo (Hot-reload)
CMD ["npm", "run", "dev"]