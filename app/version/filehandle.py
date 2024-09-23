import os

EXE_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app', 'exe_files', '1.0.0'))

print(f"Répertoire EXE_FOLDER configuré sur : {EXE_FOLDER}")

def get_latest_version():
    exe_files = []
    for root, dirs, files in os.walk(EXE_FOLDER):
        # Filtrer uniquement les répertoires de version (par exemple, "1.0.0")
        if root != EXE_FOLDER:
            for file in files:
                if file.endswith('.exe'):
                    full_path = os.path.join(root, file)
                    exe_files.append(full_path)
                    print(f"Fichier .exe trouvé : {full_path}")

    if not exe_files:
        print("Aucun fichier .exe trouvé")
        return None

    def version_key(file_path):
        file_name = os.path.basename(file_path)
        # Modification de cette ligne pour extraire correctement la version
        version_str = os.path.basename(os.path.dirname(file_path))
        return tuple(map(int, version_str.split('.')))

    latest_file = max(exe_files, key=version_key)
    print(f"Le fichier .exe le plus récent est : {latest_file}")
    return latest_file
