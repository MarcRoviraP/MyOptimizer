from platformdirs import  user_data_dir
import os
import json
import shutil

class Configuracion():
    def __init__(self):
        
        app_name = "MyOptimizer"
        print("Starting My Optimizer...")
        self.RUTA_BASE = user_data_dir(app_name,roaming=True,appauthor="MarcRoviraP")
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

    def organizarCarpetas(self):
        carpetas = []
        if self.destinyPath == "":
            print("No se ha seleccionado una carpeta de destino.")
            return
        
        with open(self.currentProfile, "r") as file:
            self.actualConfig = json.load(file)
            carpetas = [i for i in self.actualConfig]
        for carpeta in carpetas:
            if not os.path.exists(os.path.join(self.destinyPath, carpeta)):
                os.makedirs(os.path.join(self.destinyPath, carpeta))
                
    def getProfiles(self):
        perfiles = []
        for file in os.listdir(self.RUTA_CONFIG):
            if file.startswith("config_") and file.endswith(".json"):
                perfiles.append(file)
        return perfiles
                
                
if __name__ == "__main__":
    config = Configuracion()
    config.organizarCarpetas()