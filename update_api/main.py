from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from version_manager.file_handler import get_latest_version

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API de mise à jour"}

@app.get("/latest-version")
def get_latest_setup():
    latest_file = get_latest_version()
    if not latest_file:
        raise HTTPException(status_code=404, detail="Aucun fichier .exe disponible")

    return {"latest_version": latest_file.split('_')[1].replace('.exe', '')}

@app.get("/download-latest")
def download_latest_setup():
    latest_file = get_latest_version()
    if not latest_file:
        raise HTTPException(status_code=404, detail="Aucun fichier .exe disponible")

    file_path = f"./exe_files/{latest_file}"
    return FileResponse(file_path, media_type='application/octet-stream', filename=latest_file)
