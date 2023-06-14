from sawtooth_sdk.processor.handler import TransactionHandler

from models.recordModel import Record
from utils import _hash

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
        payload = RecordFactory.from_bytes(transaction.payload)
        payload.apply(context, self._namespace_prefix)
        
class RecordFactory:
    @staticmethod
    def getPayload(payload):
        try:
            # The payload is csv utf-8 encoded string
            data = json.loads(payload.decode())
            action = data["action"]
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
        return Record(action, body)
    @staticmethod
    def from_bytes(payload):
        return RecordFactory.getPayload(payload=payload)
