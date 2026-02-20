from platformdirs import user_data_dir
import os
import json
import shutil
import hashlib
from pathlib import Path
from collections import defaultdict


class Configuracion:
    def __init__(self):

        app_name = "MyOptimizer"
        print("Starting My Optimizer...")
        self.RUTA_BASE = user_data_dir(
            app_name, roaming=True, appauthor="MarcRoviraP")
        self.RUTA_CONFIG = os.path.join(self.RUTA_BASE, "config")
        self.currentProfile = os.path.join(
            self.RUTA_CONFIG, "config_Optimizador.json")
        self.destinyPath = ""
        self.actualConfig = {}
        self.folderStructure = []

        if not os.path.exists(self.RUTA_CONFIG):
            os.makedirs(self.RUTA_CONFIG)
        if not os.path.exists(os.path.join(self.RUTA_CONFIG, "config_Optimizador")):

            shutil.copy(
                os.path.join(os.path.dirname(os.path.abspath(
                    __file__)), "config_Optimizador.json"),
                self.RUTA_CONFIG,
            )

    def setDestinyPath(self, path):
        self.destinyPath = path
        print(self.destinyPath)

    def addFolderToStructure(self, folderPath):
        if folderPath not in self.folderStructure:
            self.folderStructure.append(folderPath)
            return True
        return False

    def removeFolderFromStructure(self, folderPath):
        if folderPath in self.folderStructure:
            self.folderStructure.remove(folderPath)
            return True
        return False

    def applyOrganization(self, modo="copiar", on_progress=None):
        """Organiza los archivos según el perfil activo.
        modo: 'copiar' → shutil.copy2 | 'mover' → shutil.move
        on_progress(categoria, idx, total): callback de progreso opcional
        """
        if not self.destinyPath:
            raise ValueError("No hay ruta de destino configurada")

        estructura = self.getStructureFolder()  # {categoria: [Path, ...]}
        categorias = list(estructura.items())
        total = len(categorias)

        for idx, (categoria, archivos) in enumerate(categorias, start=1):
            if on_progress:
                on_progress(categoria, idx, total)

            carpeta_destino = Path(self.destinyPath) / categoria
            carpeta_destino.mkdir(parents=True, exist_ok=True)

            for archivo in archivos:
                destino = carpeta_destino / archivo.name
                if modo == "mover":
                    shutil.move(str(archivo), str(destino))
                else:
                    shutil.copy2(str(archivo), str(destino))

    def setPerfil(self, perfil):
        self.currentProfile = os.path.join(self.RUTA_CONFIG, perfil)
        print(self.currentProfile)

    def getProfiles(self):
        perfiles = []
        for file in os.listdir(self.RUTA_CONFIG):
            if file.startswith("config_") and file.endswith(".json"):
                perfiles.append(file)
        return perfiles

    def viewProfile(self, perfil):
        with open(os.path.join(self.RUTA_CONFIG, perfil), "r") as file:
            config = json.load(file)
            return config

    def getStructureFolder(self):
        from concurrent.futures import ThreadPoolExecutor
        import threading

        with open(self.currentProfile, "r") as file:
            self.actualConfig = json.load(file)

        mapa_extensiones = {
            ext: clave
            for clave, extensiones in self.actualConfig.items()
            for ext in extensiones
        }

        # ── Paso 1: recopilar candidatos (solo stat, sin leer disco) ─────────
        candidatos = []  # [(Path, categoria)]
        for ruta in self.folderStructure:
            for f in Path(ruta).iterdir():
                if f.is_file():
                    ext = f.suffix.lower().lstrip(".")
                    cat = mapa_extensiones.get(ext)
                    if cat:
                        candidatos.append((f, cat))

        # ── Paso 2: agrupar por tamaño (sin leer contenido) ─────────────────
        por_tamanyo: dict[int, list] = defaultdict(list)
        for f, cat in candidatos:
            por_tamanyo[f.stat().st_size].append((f, cat))

        # ── Helpers de hash ──────────────────────────────────────────────────
        def _hash_parcial(path: Path) -> str:
            """Hash de los primeros 64 KB — descarta el 99% de falsos positivos."""
            h = hashlib.sha256()
            with open(path, "rb") as fh:
                h.update(fh.read(65536))
            return h.hexdigest()

        def _hash_completo(path: Path) -> str:
            h = hashlib.sha256()
            with open(path, "rb") as fh:
                for chunk in iter(lambda: fh.read(65536), b""):
                    h.update(chunk)
            return h.hexdigest()

        # ── Paso 3: deduplicar y construir resultado ─────────────────────────
        finalFolder: dict[str, list] = defaultdict(list)
        seen_full: set[str] = set()   # hashes completos confirmados
        lock = threading.Lock()

        def procesar_grupo(grupo):
            """Procesa un grupo de archivos del mismo tamaño."""
            if len(grupo) == 1:
                # Único archivo de ese tamaño → imposible que sea duplicado
                f, cat = grupo[0]
                with lock:
                    finalFolder[cat].append(f)
                return

            # Hay ≥2 archivos del mismo tamaño → comparar hash parcial primero
            por_parcial: dict[str, list] = defaultdict(list)
            for f, cat in grupo:
                por_parcial[_hash_parcial(f)].append((f, cat))

            for parciales in por_parcial.values():
                if len(parciales) == 1:
                    # Hash parcial único → no hay duplicado real
                    f, cat = parciales[0]
                    with lock:
                        finalFolder[cat].append(f)
                else:
                    # Colisión de hash parcial → verificar con hash completo
                    for f, cat in parciales:
                        full = _hash_completo(f)
                        with lock:
                            if full in seen_full:
                                print(f"🗑️ Duplicado ignorado: {f.name}")
                                continue
                            seen_full.add(full)
                            finalFolder[cat].append(f)

        grupos = list(por_tamanyo.values())
        with ThreadPoolExecutor() as executor:
            executor.map(procesar_grupo, grupos)

        return finalFolder
        '''for clave in finalFolder:
            print(clave)
            for valor in finalFolder[clave]:
                print(f"        {valor}")'''
