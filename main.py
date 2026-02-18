from platformdirs import user_data_dir
import os
import json
import shutil
from pathlib import Path
from collections import defaultdict


class Configuracion:
    def __init__(self):

        app_name = "MyOptimizer"
        print("Starting My Optimizer...")
        self.RUTA_BASE = user_data_dir(app_name, roaming=True, appauthor="MarcRoviraP")
        self.RUTA_CONFIG = os.path.join(self.RUTA_BASE, "config")
        self.currentProfile = os.path.join(self.RUTA_CONFIG, "config_Optimizador.json")
        self.destinyPath = ""
        self.actualConfig = {}
        self.folderStructure = []

        if not os.path.exists(self.RUTA_CONFIG):
            os.makedirs(self.RUTA_CONFIG)
        if not os.path.exists(os.path.join(self.RUTA_CONFIG, "config_Optimizador")):

            shutil.copy("config_Optimizador.json", self.RUTA_CONFIG)

    def setDestinyPath(self, path):
        self.destinyPath = path
        print(self.destinyPath)

    def addFolderToStructure(self, folderPath):
        if folderPath not in self.folderStructure:
            self.folderStructure.append(folderPath)
            return True
        return False

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

        with open(self.currentProfile, "r") as file:
            self.actualConfig = json.load(file)

        mapa_extensiones = {
            ext: clave
            for clave, extensiones in self.actualConfig.items()
            for ext in extensiones
        }

        finalFolder = defaultdict(list)  # ← definido antes

        def tarea(ruta):
            ruta = Path(ruta)

            for f in ruta.iterdir():
                if f.is_file():
                    extension = f.suffix.lower().lstrip(".")
                    categoria = mapa_extensiones.get(extension)
                    if categoria:
                        finalFolder[categoria].append(f)  # ← modifica el de afuera

        tarea(self.folderStructure[0])

        for clave in finalFolder:
            print(clave)
            
            for valor in finalFolder.get(clave):
                print(f"        {valor}")