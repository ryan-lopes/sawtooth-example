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
        
        if requests:
            requests = [Request.from_bytes(request) for request in requests]
        
        self._id = id
        self._title = title
        self._bundle_hash = bundle_hash
        self._requests = requests or []
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
    @staticmethod
    def from_bytes(record):
        return Record(json.loads(record.decode('utf-8')))
    
    def requested(self, id_request, doctor_cpf):
        request = Request(id_request, doctor_cpf)
        self._requests.append(request)

    def granted(self, id_request, request_status):
        for request in self._requests:
            if request.id == id_request:
                request.reply(request_status)
                return None
        print('Record does not exist')
        return None