FROM python:3.11-slim

WORKDIR /app

# Copiar el código fuente y el script de espera
COPY . /app
COPY wait-for-it.sh /wait-for-it.sh

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Hacer ejecutable el script de espera
RUN chmod +x /wait-for-it.sh

EXPOSE 8000

# Usar wait-for-it.sh para esperar que PostgreSQL esté disponible antes de iniciar
CMD ["/wait-for-it.sh", "db:5432", "--", "sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
