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
RUN mkdir -p ~/.config/hca
COPY src/config_sample.toml ~/.config/hca/config.toml

# Port für Streamlit freigeben
EXPOSE 8080


# Startbefehl für die Streamlit-App
CMD ["streamlit", "run", "web_app.py", "--server.port=8080", "--server.address=0.0.0.0"]
