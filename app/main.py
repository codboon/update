from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from app.version.filehandle import get_latest_version
import os

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API de mise à jour"}

@app.get("/latest-version")
def get_latest_setup():
    latest_file = get_latest_version()
    print(f"Fichier de la dernière version trouvé : {latest_file}")
    if not latest_file:
        print("Aucun fichier .exe disponible")
        raise HTTPException(status_code=404, detail="Aucun fichier .exe disponible")

    version_number = os.path.basename(os.path.dirname(latest_file))
    print(f"Version extraite : {version_number}")
    return {"latest_version": version_number}


@app.get("/download-latest")
def download_latest_setup():
    latest_file = get_latest_version()
    print(f"Tentative de téléchargement du fichier : {latest_file}")
    if not latest_file:
        print("Aucun fichier .exe disponible")
        raise HTTPException(status_code=404, detail="Aucun fichier .exe disponible")

    file_path = latest_file
    print(f"Chemin complet du fichier : {file_path}")
    return FileResponse(file_path, media_type='application/octet-stream', filename=os.path.basename(latest_file))
