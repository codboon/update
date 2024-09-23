import os

# Mettre à jour le chemin de EXE_FOLDER pour pointer vers le bon répertoire
EXE_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'exe_files'))


def get_latest_version():
    exe_files = []
    print(f"Répertoire EXE_FOLDER configuré sur : {EXE_FOLDER}")

    # Parcourir les répertoires pour rechercher les fichiers .exe
    for root, dirs, files in os.walk(EXE_FOLDER):
        for file in files:
            if file.endswith('.exe'):
                full_path = os.path.join(root, file)
                exe_files.append(full_path)
                print(f"Fichier .exe trouvé : {full_path}")

    if not exe_files:
        print("Aucun fichier .exe trouvé")
        return None

    def version_key(file_path):
        # Extraire la version à partir du chemin du répertoire parent
        version_str = os.path.basename(os.path.dirname(file_path))
        try:
            return tuple(map(int, version_str.split('.')))
        except ValueError:
            # Si la version ne peut pas être convertie en tuple d'entiers, retournez un tuple vide (0, 0, 0)
            return (0, 0, 0)

    # Trouver le fichier avec la version la plus récente
    latest_file = max(exe_files, key=version_key)
    print(f"Le fichier .exe le plus récent est : {latest_file}")
    return latest_file
