from sawtooth_sdk.processor.handler import TransactionHandler

from models.doctor_model import Doctor
from models.patient_model import Patient
from utils import _hash

import json

FAMILY_NAME = 'FAMILY_CONTROLLER'

class ControllerTransactionHandler(TransactionHandler):
    def __init__(self):
        self._namespace_prefix = _hash(FAMILY_NAME.encode('utf-8'))[0:6]
    @property
    def family_name(self):
        return FAMILY_NAME

    @property
    def family_versions(self):
        return ['1.0']

    @property
    def namespaces(self):
        return [self._namespace_prefix]
    
    def getNamespace(self):
        return self._namespace_prefix

    def apply(self, transaction, context):
        try:
            header = transaction.header
            signer = header.signer_public_key
            action, payload = ControllerFactory.from_bytes(transaction.payload)
            address = self._namespace_prefix + _hash(payload.cpf.encode('utf-8'))[:64]
            state = context.get_state([address])
        except:
            print("Um erro ocorreu")
            return
            
        if action == 'add':
            if state:
                print(f'{payload._type} already exists')
                return None
            state_data = payload.to_bytes()
            context.set_state({address: state_data})
            print(f'{payload._type} was added')
        
        elif action == 'show':
            if not state:
                print(f'{payload._type} does not exist')
                return None
            state_data = state[0].data.decode('utf-8')
            print(f'{payload._type} data: {ControllerFactory.getPatient(state)}')
        
        elif action == 'delete':
            if not state:
                print('{} does not exist' %format(payload._type))
                return None
            context.delete_state([address])
            print(f'{payload._type} was deleted')

        
class ControllerFactory:
    @staticmethod
    def getPatient(state):
        if not state:
            print('Patient does not exist')
            return None
        state_data = state[0].data
        return Patient.from_bytes(state_data)
    @staticmethod
    def getPayload(payload):
        try:
            # The payload is csv utf-8 encoded string
            data = json.loads(payload.decode())
            action = data["action"]
            type = data["type"]
            body = data["body"]
        except ValueError:
            print("Invalid payload serialization")
            return None
        
        if not action:
            print('Action is required')
            return None

        if action not in ('add', 'show', 'delete'):
            print('Invalid action: {}' % format(action))
            return None
        
        if type not in ('doctor','patient'):
            print('Invalid type: {}'%format(type))
            return None
        
        if type == 'doctor':
            return action, Doctor(body)
        
        if type == 'patient':
            return action, Patient(body)
    @staticmethod
    def from_bytes(payload):
        return ControllerFactory.getPayload(payload=payload)
