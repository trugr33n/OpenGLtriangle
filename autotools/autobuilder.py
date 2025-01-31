import os
import subprocess as sub
import shutil as copier
import logging as log

log.basicConfig(level=log.INFO)

class AutobuilderMeta(type):
    _instances = {}
    def __call__(cls, *args, **kwds):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwds)
        return cls._instances[cls]

class Autobuilder(metaclass=AutobuilderMeta):
    def __init__(self, gen: str):
        self._generator: str = gen
        self._currentDir: str = os.getcwd()
        self._buildFolder: str = os.path.join(self._currentDir, "build")
        self._dllFolder: str = os.path.join(self._currentDir, f"dll/{gen}")

        if gen == "VS":
            self._destFolder: str = os.path.join(self._buildFolder, "Debug")
            self._buildCommands: list[list[str]] = [
                ["cmake", "..", "-G", "Visual Studio 17 2022"],
                ["cmake", "--build", "."],
            ]
        elif gen == "MinGW":
            self._buildCommands: list[list[str]] = [
                ["cmake", "..", "-G", "MinGW Makefiles"],
                ["mingw32-make"],
            ]

        self._dllFiles: list = [f for f in os.listdir(self._dllFolder) if os.path.isfile(os.path.join(self._dllFolder, f))]
    
    def build(self):
        sub.run("cls" if os.name == "nt" else "clear", shell=True)

        if os.path.isdir(self._buildFolder):
            log.info(f"Folder {self._buildFolder} exists.")
        else:
            log.info(f"Folder {self._buildFolder} doesn't exist. Creating build folder... ")
            os.makedirs(self._buildFolder)
            log.info("Folder created\n")

        os.chdir(self._buildFolder)

        for command in self._buildCommands:
            try:
                result = sub.run(command, shell=True, text=True)
                result.check_returncode()
                log.info(f"Command \"{' '.join(command)}\" ended with success!")
            except sub.CalledProcessError:
                log.error(f"Error while running command \"{' '.join(command)}\"")
                exit(1)
        
        self._dll_checkout()
        
    def _dll_checkout(self):
        targetFolder: str = self._target_folder_checkout

        for thing in self._dllFiles:
            if os.path.isfile(os.path.join(targetFolder, thing)):
                log.info(f"dll file {thing} exists in {targetFolder}")
            else:
                log.info(f"dll file {thing} doesn't exist in {targetFolder}. Copying to folder... ")
                copier.copy(os.path.join(self._dllFolder, thing), targetFolder)
                log.info(f"dll file {thing} copied successfully")
    
    @property
    def _target_folder_checkout(self) -> str:
        match(self._generator):
            case "VS":
                return self._destFolder
            case "MinGW":
                return self._buildFolder
