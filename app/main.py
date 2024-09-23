from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.version.filehandle import get_latest_version
import os

# Configuration du rate limiter
limiter = Limiter(key_func=get_remote_address)
app = FastAPI()

# Ajout du gestionnaire d'erreurs pour le rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.get("/")
@limiter.limit("10/minute")  # Limite à 10 requêtes par minute
def read_root(request: Request):
    return {"message": "Bienvenue sur l'API de mise à jour"}

@app.get("/latest-version")
@limiter.limit("5/minute")  # Limite à 5 requêtes par minute
def get_latest_setup(request: Request):
    latest_file = get_latest_version()
    print(f"Fichier de la dernière version trouvé : {latest_file}")
    if not latest_file:
        print("Aucun fichier .exe disponible")
        raise HTTPException(status_code=404, detail="Aucun fichier .exe disponible")

    version_number = os.path.basename(os.path.dirname(latest_file))
    print(f"Version extraite : {version_number}")
    return {"latest_version": version_number}

@app.get("/download-latest")
@limiter.limit("3/minute")  # Limite à 3 requêtes par minute
def download_latest_setup(request: Request):
    latest_file = get_latest_version()
    print(f"Tentative de téléchargement du fichier : {latest_file}")
    if not latest_file:
        print("Aucun fichier .exe disponible")
        raise HTTPException(status_code=404, detail="Aucun fichier .exe disponible")

    file_path = latest_file
    print(f"Chemin complet du fichier : {file_path}")
    return FileResponse(file_path, media_type='application/octet-stream', filename=os.path.basename(latest_file))
