import json
from utils import _hash

class Record:
    def __init__(self, action, body):
        title = body["title"]
        bundle_hash = body["bundle_hash"]
        cpf = body["cpf"]

        if not bundle_hash:
            print('Bundle Hash is required')
            return None

        if not title:
            print('Title is required')
            return None

        if not cpf:
            print('CPF is required')
            return None
        
        self._title = title
        self._bundle_hash = bundle_hash
        self._requests = []
        self._action = action
        self._cpf_owner = cpf ## Verificar
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