import pytest
from fastapi.testclient import TestClient
from app.main import app
import os

EXE_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app', 'exe_files', '1.0.0'))

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Bienvenue sur l'API de mise à jour"}

def test_get_latest_version_no_files(monkeypatch):
    def mock_get_latest_version():
        return None

    monkeypatch.setattr("app.version.filehandle.get_latest_version", mock_get_latest_version)

    response = client.get("/latest-version")
    assert response.status_code == 404
    assert response.json() == {"detail": "Aucun fichier .exe disponible"}

def test_get_latest_version_with_files(monkeypatch):
    def mock_get_latest_version():
        return os.path.join(EXE_FOLDER, "codboon_1.0.0.exe")

    # Remplacer le chemin ci-dessous par le chemin complet de la fonction réelle dans votre application
    monkeypatch.setattr("app.main.get_latest_version", mock_get_latest_version)

    response = client.get("/latest-version")
    assert response.status_code == 200
    assert response.json() == {"latest_version": "1.0.0"}

def test_download_latest_setup_no_files(monkeypatch):
    def mock_get_latest_version():
        return None

    monkeypatch.setattr("app.version.filehandle.get_latest_version", mock_get_latest_version)

    response = client.get("/download-latest")
    assert response.status_code == 404
    assert response.json() == {"detail": "Aucun fichier .exe disponible"}

def test_download_latest_setup_with_files(monkeypatch):
    def mock_get_latest_version():
        return os.path.join(EXE_FOLDER, "codboon_1.0.0.exe")

    # Remplacer le chemin ci-dessous par le chemin complet de la fonction réelle dans votre application
    monkeypatch.setattr("app.main.get_latest_version", mock_get_latest_version)

    response = client.get("/download-latest")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/octet-stream"
    assert response.headers["content-disposition"] == 'attachment; filename="codboon_1.0.0.exe"'
