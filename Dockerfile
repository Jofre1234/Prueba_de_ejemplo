FROM python:3.9-slim

# Carpeta de trabajo
WORKDIR /app

# Instalamos los requerimientos primero (para aprovechar caché)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto del código
COPY . .

# IMPORTANTE: Exponemos el puerto 5000
EXPOSE 5000

# COMANDO DE ARRANQUE: Obligamos a ejecutar app.py directamente
CMD ["python", "app.py"]