import json
from utils import _hash

class Patient:
    def __init__(self, body):
        cpf = body["cpf"]
        name = body["name"]
        records = body["records"]
        
        if not cpf:
            print('CPF is required')
            return None

        if not name:
            print('Name is required')
            return None
        
        if records:
            records = [record.from_bytes() for record in records]

        self._name = name
        self._cpf = cpf
        self._records = records or []
        self.type = "Patient"

    @property
    def cpf(self):
        return self._cpf

    @property
    def name(self):
        return self._name

    def from_bytes(self, data):
        body = json.loads(data.decode('utf-8'))
        return Patient(body)
    
    def to_bytes(self):
        patient = {
            "name": self._name, 
            "cpf": self._cpf,
            "records": [record.to_bytes() for record in self._records]
        }
        
        return json.dumps(patient).encode()
    
    def update_patient(self, state, address, context):
        state_data = state.to_bytes()
        context.set_state({address: state_data})

    def add_record(self, record):
        self._records.append(record)
        

    def get_record(self, id_record):
        for record in self._records:
            if record.id == id_record:
                return record
        print('Record does not exist')
        return None

    def delete_record(self, id_record):
        for record in self._records:
            if record.id == id_record:
                self._records.remove(record)
                return None
        print('Record does not exist')
        return None
        

    def request_record(self, id_record, doctor_cpf):
        self._records.append(record)

    def grant_record(self, record):
        self._records.append(record)
