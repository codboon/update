# Utiliser une image officielle de Python 3.10 comme base
FROM python:3.10

# Définir le répertoire de travail à l'intérieur du conteneur
WORKDIR /app

# Copier le fichier requirements.txt dans le conteneur
COPY requirements.txt .

# Installer les dépendances à partir du fichier requirements.txt
RUN pip install -r requirements.txt

# Copier tous les fichiers de l'application dans le conteneur
COPY . .

# Exposer le port 8000 (FastAPI utilise généralement ce port)
EXPOSE 8000