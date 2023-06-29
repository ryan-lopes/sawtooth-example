
import json
from utils import _hash

class Request:
    def __init__(self, body):
        doctor_cpf = body.get("doctor_cpf", None)
        request_id = body.get("request_id", None)
        request_status = body.get("request_status", None)
        
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
        self._request_status = status

    def to_json(self):
        request = {
            "doctor_cpf": self._doctor_cpf, 
            "request_id": self._request_id,
            "request_status": self._request_status
        }
        
        return json.dumps(request)
    
    @staticmethod
    def from_json(data):
        data_dict = json.loads(data)
        
        # Extract the values for doctor_cpf and request_id
          
        request = Request(data_dict)

        return request

    def __repr__(self):
        return f"ID: {self._request_id}, Doctor_CPF: {self._doctor_cpf}, request_status: {self._request_status}"