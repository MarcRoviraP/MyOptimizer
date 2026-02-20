import os
import hashlib

def hash_file(path):
    """Genera hash SHA256 de un archivo"""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            h.update(chunk)
    return h.hexdigest()

def find_unique_files(folder):
    """Devuelve un diccionario hash -> archivo original único"""
    seen_hashes = {}
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        if os.path.isfile(file_path):
            file_hash = hash_file(file_path)
            if file_hash not in seen_hashes:
                seen_hashes[file_hash] = file_path
            else:
                print(f"Duplicado detectado: {file_path} es igual que {seen_hashes[file_hash]} File: {file_hash}")
    return list(seen_hashes.values())

# Carpeta a escanear
folder = "C:\\Users\\Marc\\Desktop\\Destiny\\Documentos_PDF"

unique_files = find_unique_files(folder)
print("\nArchivos únicos encontrados:")
for f in unique_files:
    print(f)
