
import json
from utils import _hash

class Request:
    def __init__(self, body):
        doctor_cpf = body["doctor_cpf"]
        request_id = body["request_id"]
        request_status = body["request_status"]
        
        if request_status == None:
            request_status = 0

        self._doctor_cpf = doctor_cpf
        self._request_id = request_id
        self._request_status = request_status #0 for waiting approval, 1 for approved, 2 for denied.

    @property
    def doctor(self):
        return self._doctor_cpf

    @property
    def id(self):
        return self._request_id
    
    @property
    def status(self):
        return self._request_status
    
    def reply(self, status):
        self._request_id = status

    def to_bytes(self):
        request = {
            "doctor_cpf": self._doctor_cpf, 
            "request_id": self._request_id,
            "request_status": self._request_status
        }
        
        return json.dumps(request).encode()
    
    def from_bytes(self, data):
        data_dict = json.loads(data.decode())
        
        # Extract the values for doctor_cpf and request_id
        doctor_cpf = data_dict['doctor_cpf']
        request_id = data_dict['request_id']
        request_status = data_dict['request_status']
        request = Request(doctor_cpf, request_id, request_status)

        return request

