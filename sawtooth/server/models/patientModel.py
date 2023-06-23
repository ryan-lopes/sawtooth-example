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
        
        if not records:
            records = []

        self._name = name
        self._cpf = cpf
        self._records = records

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
            "records": self._records
        }
        
        return json.dumps(patient).encode()
    
    def apply(self, action, state, address, context):
        if action == 'add':
            if state:
                print('Patient already exists')
                return None
            state_data = self.to_bytes()
            context.set_state({address: state_data})
        
        elif action == 'update':
            state_data = self.to_bytes()
            context.set_state({address: state_data})
        
        elif action == 'get':
            if not state:
                print('Patient does not exist')
                return None
            state_data = state[0].data.decode('utf-8')
            return state_data
        
        elif action == 'show':
            if not state:
                print('Patient does not exist')
                return None
            state_data = state[0].data.decode('utf-8')
            print(f'Patient data: {state_data}')

        elif action == 'delete':
            if not state:
                print('Patient does not exist')
                return None
            context.delete_state([address])

        print("Apply realizado com sucesso")
