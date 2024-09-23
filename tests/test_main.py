import pytest
from fastapi.testclient import TestClient
from app.main import app
import os

# Initialize the test client
client = TestClient(app)

def get_latest_version_folder_and_exe():
    """Fetches the latest version folder and exe file based on the highest version number available in the exe_files directory."""
    base_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app', 'exe_files'))
    
    if not os.path.exists(base_folder):
        return None, None
    
    # List all version directories
    version_dirs = [d for d in os.listdir(base_folder) if os.path.isdir(os.path.join(base_folder, d))]
    
    if not version_dirs:
        return None, None
    
    # Convert version strings to tuples for comparison
    version_tuples = []
    for version in version_dirs:
        try:
            version_tuples.append((tuple(map(int, version.split('.'))), version))
        except ValueError:
            continue
    
    if version_tuples:
        # Get the latest version folder
        latest_version_folder = max(version_tuples, key=lambda x: x[0])[1]
        full_path_to_folder = os.path.join(base_folder, latest_version_folder)
        
        # Find the executable file in this folder
        exe_file_name = f"codboon_v{latest_version_folder}.exe"
        exe_file_path = os.path.join(full_path_to_folder, exe_file_name)
        
        if os.path.exists(exe_file_path):
            return full_path_to_folder, exe_file_path
    
    return None, None

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Bienvenue sur l'API de mise à jour"}

def test_get_latest_version_with_files(monkeypatch):
    latest_version_folder, latest_exe_file = get_latest_version_folder_and_exe()
    if not latest_exe_file:
        pytest.skip("No valid executable file found for testing.")
    
    def mock_get_latest_version():
        return latest_exe_file

    monkeypatch.setattr("app.main.get_latest_version", mock_get_latest_version)

    response = client.get("/latest-version")
    assert response.status_code == 200
    version_number = os.path.basename(latest_version_folder)  # Extract the version number from the folder name
    assert response.json() == {"latest_version": version_number}


def test_download_latest_setup_with_files(monkeypatch):
    latest_version_folder, latest_exe_file = get_latest_version_folder_and_exe()
    if not latest_exe_file:
        pytest.skip("No valid executable file found for testing.")
    
    def mock_get_latest_version():
        return latest_exe_file

    monkeypatch.setattr("app.main.get_latest_version", mock_get_latest_version)

    response = client.get("/download-latest")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/octet-stream"
    assert response.headers["content-disposition"] == f'attachment; filename="{os.path.basename(latest_exe_file)}"'

def test_rate_limiting_root():
    rate_limit_triggered = False
    for _ in range(11):  # Exécute un nombre de requêtes supérieur à la limite
        response = client.get("/")
        if response.status_code == 429:
            rate_limit_triggered = True
            break
    
    assert rate_limit_triggered, "Le rate limiting n'a pas été déclenché comme prévu"


def test_rate_limiting_latest_version(monkeypatch):
    def mock_get_latest_version():
        _, latest_exe_file = get_latest_version_folder_and_exe()
        return latest_exe_file

    monkeypatch.setattr("app.main.get_latest_version", mock_get_latest_version)

    rate_limit_triggered = False
    for _ in range(6):  # Exécute un nombre de requêtes supérieur à la limite
        response = client.get("/latest-version")
        if response.status_code == 429:
            rate_limit_triggered = True
            break
    
    assert rate_limit_triggered, "Le rate limiting n'a pas été déclenché comme prévu"


def test_rate_limiting_download_latest(monkeypatch):
    def mock_get_latest_version():
        _, latest_exe_file = get_latest_version_folder_and_exe()
        return latest_exe_file

    monkeypatch.setattr("app.main.get_latest_version", mock_get_latest_version)

    rate_limit_triggered = False
    for _ in range(4):  # Exécute un nombre de requêtes supérieur à la limite
        response = client.get("/download-latest")
        if response.status_code == 429:
            rate_limit_triggered = True
            break
    
    assert rate_limit_triggered, "Le rate limiting n'a pas été déclenché comme prévu"
