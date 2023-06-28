import json
from utils import _hash

class Doctor:
    def __init__(self, body):
        cpf = body.get("cpf", None)
        name = body.get("name", None)
        
        if not cpf:
            print('CPF is required')
            return None

        if not name:
            print('Name is required')
            return None
        
        self._name = name
        self._cpf = cpf
        self.type = "Doctor"
    @property
    def cpf(self):
        return self._cpf

    @property
    def name(self):
        return self._name

    def to_bytes(self):
        doctor = {
            "name": self._name, 
            "cpf": self._cpf
        }
        
        return json.dumps(doctor).encode()
    