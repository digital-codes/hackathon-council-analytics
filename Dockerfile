# Basis-Image: Python 3.12
FROM python:3.12-slim

RUN apt-get update
RUN apt-get install -y build-essential

# Arbeitsverzeichnis im Container setzen
WORKDIR /app

# Requirements-Datei kopieren und Abhängigkeiten installieren
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Den gesamten Code ins Arbeitsverzeichnis kopieren
COPY src .
RUN mkdir -p /root/.config/hca

# Port für Streamlit freigeben
EXPOSE 8501

# Startbefehl für die Streamlit-App
CMD ["streamlit", "run", "web_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
