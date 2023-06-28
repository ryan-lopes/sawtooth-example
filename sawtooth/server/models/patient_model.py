import json
from utils import _hash

from models.record_model import Record

class Patient:
    def __init__(self, body):
        cpf = body.get("cpf", None)
        name = body.get("name", None)
        records = body.get("records", None)
        
        if not cpf:
            print('CPF is required')
            return None

        if not name:
            print('Name is required')
            return None
        
        if records:
            records = [Record.from_json(record) for record in records]

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
    
    @staticmethod
    def from_bytes(data):
        body = json.loads(data.decode('utf-8'))
        return Patient(body)
    
    def to_bytes(self):
        patient = {
            "name": self._name, 
            "cpf": self._cpf,
            "records": [record.to_json() for record in self._records]
        }
        return json.dumps(patient).encode()
    
    def update_patient(self, state, address, context):
        state_data = self.to_bytes()
        context.set_state({address: state_data})

    def add_record(self, record):
        self._records.append(record)
        
    def get_record(self, id_record):
        for record in self._records:
            if record._id_record == id_record:
                return record
        print('Record does not exist')
        return None

    def delete_record(self, id_record):
        for record in self._records:
            if record._id_record == id_record:
                self._records.remove(record)
                return None
        print('Record does not exist')
        return None
        

    def request_record(self, id_record, doctor_cpf, id_request):
        for record in self._records:
            if record._id_record == id_record:
                record.requested(id_request, doctor_cpf)
                return None
        print('Record does not exist')
        return None

    def grant_record(self, id_record, doctor_cpf, id_request, request_status):
        for record in self._records:
            if record._id_record == id_record:
                record.granted(id_request, request_status)
                return None
        print('Record does not exist')
        return None
