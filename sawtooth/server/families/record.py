from sawtooth_sdk.processor.handler import TransactionHandler

from models.recordModel import Record
from utils import _hash
from controller import ControllerTransactionHandler, ControllerFactory

import json

FAMILY_NAME = 'FAMILY_RECORD'

class RecordTransactionHandler(TransactionHandler):
    def __init__(self):
        self._namespace_prefix = _hash(FAMILY_NAME.encode('utf-8'))[0:6]

    @property
    def family_name(self):
        return FAMILY_NAME

    @property
    def family_versions(self):
        return ['1.0']

    @property
    def namespace(self):
        return self._namespace_prefix

    def apply(self, transaction, context):
        header = transaction.header
        signer = header.signer_public_key
        action, patient_cpf, record = RecordFactory.from_bytes(transaction.payload)

        controller_namespace_prefix = ControllerTransactionHandler.namespace
        patient_address = controller_namespace_prefix + _hash(patient_cpf.encode('utf-8'))[:64]
        state = context.get_state([patient_address])
        
        patient = ControllerFactory.getPatient(state)
        record.apply(action, patient)
        patient.apply(action="update", state=state, address=patient_address, context=context)
        
class RecordFactory:
    @staticmethod
    def getPayload(payload):
        try:
            # The payload is csv utf-8 encoded string
            data = json.loads(payload.decode())
            action = data["action"]
            patient_cpf = data["patient_cpf"]
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
        return action, patient_cpf, Record(body)
    @staticmethod
    def from_bytes(payload):
        return RecordFactory.getPayload(payload=payload)
