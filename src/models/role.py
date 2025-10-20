from uuid6 import uuid7
from datetime import datetime


class Role:
    def __init__(self, name:str,description:str = ""):
        self._validate_name(name)
        self.id = str(uuid7())
        self.name = name.strip().lower()
        self.description = description.strip()
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def _validate_name(self, name:str) -> None:
        if not name or not name.strip():
            #Crear un error personalizado al igual que un mensaje
            raise ValueError("El nombre del rol no puede estar vacio")
        
    def update_description(self, new_description:str):
        self.description = new_description.strip()
        self.updated_at = datetime.now()
