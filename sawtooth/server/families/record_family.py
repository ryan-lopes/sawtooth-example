from sawtooth_sdk.processor.handler import TransactionHandler

from models.record_model import Record
from utils import _hash
from families.controller_family import ControllerTransactionHandler, ControllerFactory

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
    def namespaces(self):
        return [self._namespace_prefix]

    def apply(self, transaction, context):
        header = transaction.header
        signer = header.signer_public_key
        action, patient_cpf, body = RecordFactory.from_bytes(transaction.payload)

        controller_namespace_prefix = ControllerTransactionHandler().getNamespace()
        patient_address = controller_namespace_prefix + _hash(patient_cpf.encode('utf-8'))[:64]
        state = context.get_state([patient_address])
        patient = ControllerFactory.getPatient(state)

        if action == 'add':
            record = Record(body)
            patient.add_record(record)
            print(f"Record added")
        elif action == 'show':
            id_record = body["id_record"]
            record = patient.get_record(id_record)
            print(f"Record {repr(record)}")
        elif action == 'delete':
            id_record = body["id_record"]
            patient.delete_record(id_record)
        elif action == 'grant':
            id_record = body["id_record"]
            doctor_cpf = body["doctor_cpf"]
            id_request = body["id_request"]
            request_status = body["request_status"]
            patient.grant_record(id_record, doctor_cpf, id_request, request_status)
            print(f"Record granted")
            record = patient.get_record(id_record)
            print(f"Record {repr(record)}")
        elif action == 'request':
            id_record = body["id_record"]
            doctor_cpf = body["doctor_cpf"]
            id_request = body["id_request"]
            patient.request_record(id_record, doctor_cpf, id_request)
            print(f"Record requested")
        patient.update_patient(state=state, address=patient_address, context=context)
        print(patient)
        
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

        if action not in ('add', 'show', 'delete', 'grant', 'request'):
            print(f'Invalid action: {action}')
            return None
        return action, patient_cpf, body
    @staticmethod
    def from_bytes(payload):
        return RecordFactory.getPayload(payload=payload)
