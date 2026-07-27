# Usar una imagen oficial de Python ligera
FROM python:3.11-slim

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar el archivo de dependencias primero para aprovechar la caché de Docker
COPY requirements.txt .

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el contenido del proyecto al contenedor
COPY . .

# Exponer el puerto que usa Streamlit
EXPOSE 8501

# Configuración recomendada por Streamlit para entornos en la nube (Render, Railway, etc.)
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
# Asegurarse de que Python imprima en la consola sin buffers
ENV PYTHONUNBUFFERED=1 

# Comando de inicio
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
