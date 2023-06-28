import json
from utils import _hash
from models.request_model import Request
class Record:
    def __init__(self, body):
        id_record = body.get("id_record",None)
        title = body.get("title", None)
        bundle_hash = body.get("bundle_hash", None)
        requests = body.get("requests", None)

        if not id_record:
            print('ID is required')
            return None
        
        if requests:
            requests = [Request.from_json(request) for request in requests]
        
        self._id_record = id_record
        self._title = title
        self._bundle_hash = bundle_hash
        self._requests = requests or []
    @property
    def action(self):
        return self._action

    @property
    def title(self):
        return self._title
    
    @property
    def bundle_hash(self):
        return self._bundle_hash
    
    def to_json(self):
        record = {
            "id_record": self._id_record,
            "title": self._title, 
            "bundle_hash": self._bundle_hash,
            "requests": [request.to_json() for request in self._requests]
        }
        
        return json.dumps(record)
    
    @staticmethod
    def from_json(record):
        return Record(json.loads(record))
    
    def requested(self, id_request, doctor_cpf):
        
        request = Request({
            "request_id": id_request, "doctor_cpf": doctor_cpf
        })
        self._requests.append(request)

    def granted(self, id_request, request_status):
        for request in self._requests:
            if request._request_id == id_request:
                request.reply(request_status)
                return None
        print('Record does not exist')
        return None
    def __repr__(self):
        return f"ID: {self._id_record}, bundle_hash: {self._bundle_hash}, title: {self._title}"