import json
from utils import _hash

class Doctor:
    def __init__(self, action, body):
        cpf = body["cpf"]
        name = body["name"]
        
        if not cpf:
            print('CPF is required')
            return None

        if not name:
            print('Name is required')
            return None
        
        self._name = name
        self._cpf = cpf
        self._action = action
    
    @property
    def action(self):
        return self._action

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

    def apply(self, context, namespace_prefix):
        address = namespace_prefix + _hash(self._cpf.encode('utf-8'))[:64]
        state = context.get_state([address])

        if self.action == 'add':
            if state:
                print('Doctor already exists')
                return None
            state_data = self.to_bytes()
            context.set_state({address: state_data})
            
        elif self.action == 'show':
            if not state:
                print('Doctor does not exist')
                return None
            state_data = state[0].data.decode('utf-8')
            print(f'Doctor data: {state_data}')
        
        elif self.action == 'delete':
            if not state:
                print('Doctor does not exist')
                return None

            context.delete_state([address])
        print("Apply realizado com sucesso")