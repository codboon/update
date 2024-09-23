import os

EXE_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'exe_files')

def get_latest_version():
    files = [f for f in os.listdir(EXE_FOLDER) if f.endswith('.exe')]
    
    if not files:
        return None

    def version_key(file_name):
        version_str = file_name.split('_')[1].replace('.exe', '')
        return tuple(map(int, version_str.split('.')))
    
    latest_file = max(files, key=version_key)
    return latest_file
