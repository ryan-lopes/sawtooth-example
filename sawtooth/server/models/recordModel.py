import json
from utils import _hash

class Record:
    def __init__(self, body):
        id = body["id"]
        title = body["title"]
        bundle_hash = body["bundle_hash"]
        requests = body["requests"]

        if not id:
            print('ID is required')
            return None
        
        self._id = id
        self._title = title
        self._bundle_hash = bundle_hash
        self._requests = requests
    @property
    def action(self):
        return self._action

    @property
    def cpf(self):
        return self._cpf

    @property
    def name(self):
        return self._name

    @property
    def title(self):
        return self._title
    
    @property
    def bundle_hash(self):
        return self._bundle_hash
    
    def to_bytes(self):
        record = {
            "title": self._title, 
            "bundle_hash": self._bundle_hash,
            "requests": self._requests
        }
        
        return json.dumps(record).encode()

    def apply(self, action, patient):
        if action == 'add':
            patient.add_record(self.to_bytes())
        elif action == 'show':
            record = patient.get_record(self.id)
        elif action == 'delete':
            patient.delete_record(self.id)
        elif action == 'grant':
            # patient.grant_record(self.id, id_request)
            pass
        elif action == 'request':
            # patient.request_record(self.id, cpf_doctor)
            pass
        print("Apply realizado com sucesso")