# Usar una imagen base de Node.js
FROM node:18-bullseye

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar el package.json y pnpm-lock.yaml (si existe)
COPY package.json pnpm-lock.yaml* ./

# Instalar pnpm
RUN npm install -g pnpm

# Instalar dependencias
RUN pnpm install --frozen-lockfile

# Copiar el resto de la aplicación
COPY . .

# Exponer el puerto que usará la aplicación
EXPOSE 5173

# Comando para iniciar la aplicación
CMD ["pnpm", "run", "dev"]
