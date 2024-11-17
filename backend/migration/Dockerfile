FROM python:3.9-slim

# Establecer directorio de trabajo
WORKDIR /usr/src/app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    curl \
    tar \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copiar el instalador de CPLEX al contenedor
COPY cplex_installer.bin /opt/cplex_installer.bin

# Instalar CPLEX
RUN chmod +x /opt/cplex_installer.bin && \
    /opt/cplex_installer.bin -i silent -DLICENSE_ACCEPTED=true -DUSER_INSTALL_DIR=/opt/ibm/cplex

# Configurar variables de entorno para CPLEX
ENV CPLEX_STUDIO_DIR2211=/opt/ibm/cplex
ENV PATH="/opt/ibm/cplex/cplex/bin/x86-64_linux:$PATH"
ENV PYTHONPATH="/opt/ibm/cplex/python/3.9/x86-64_linux:$PYTHONPATH"

# Instalar dependencias de Python
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código fuente
COPY . .

# Comando predeterminado
CMD ["python", "main.py"]
