from sawtooth_sdk.processor.handler import TransactionHandler

from models.doctor import Doctor
from models.patient import Patient
from utils import _hash

import json

FAMILY_NAME = 'FAMILY_RECORD'

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

    def apply(self, transaction, context):
        header = transaction.header
        signer = header.signer_public_key
        payload = ControllerFactory.from_bytes(transaction.payload)
        payload.apply(context, self._namespace_prefix)
        
class ControllerFactory:
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
            return Doctor(action, body)
        
        if type == 'patient':
            return Patient(action, body)
    @staticmethod
    def from_bytes(payload):
        return ControllerFactory.getPayload(payload=payload)
