
from sawtooth_sdk.processor.core import TransactionProcessor
from sawtooth_sdk.processor.handler import TransactionHandler
from sawtooth_sdk.processor.exceptions import InvalidTransaction
from sawtooth_sdk.processor.exceptions import InternalError
import hashlib

FAMILY_NAME = 'PIBITI_2022'

def _hash(data):
    '''Compute the SHA-512 hash and return the result as hex characters.'''
    return hashlib.sha512(data).hexdigest()

def main():
    print('ok')
    processor = TransactionProcessor(url='tcp://validator:4004')
    handler = ClientTransactionHandler(_hash(FAMILY_NAME.encode('utf-8'))[0:6])
    processor.add_handler(handler)
    processor.start()


class ClientTransactionHandler(TransactionHandler):
    def __init__(self, namespace_prefix):
        self._namespace_prefix = namespace_prefix

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
        print('apply')
        header = transaction.header
        signer = header.signer_public_key
        payload = ClientPayload.from_bytes(transaction.payload)

        print(self._namespace_prefix)
        print(payload._cpf)
        print(payload._name)
        address = self._namespace_prefix + _hash(payload._cpf.encode('utf-8'))[:64]
        state = context.get_state([address])

        if payload.action == 'add':
            
            if state:
                raise InvalidTransaction('Client already exists')

            state_data = (payload._name + ',' + payload._cpf).encode('utf-8')
            context.set_state({address: state_data})
            
        elif payload.action == 'show':

            if not state:
                raise InvalidTransaction('Client does not exist')
            
            client_data = state[0].data.decode('utf-8')
            print(f'Client data: {client_data}')

        
        
        elif payload.action == 'delete':


            if not state:
                raise InvalidTransaction('Client does not exist')

            context.delete_state([address])
        
class ClientPayload:
    def __init__(self, payload):
        try:
            # The payload is csv utf-8 encoded string
            action, cpf, name = payload.decode().split(",")
        except ValueError:
            raise InvalidTransaction("Invalid payload serialization")

        if not cpf:
            raise InvalidTransaction('CPF is required')

        if not name:
            raise InvalidTransaction('Name is required')

        if not action:
            raise InvalidTransaction('Action is required')

        if action not in ('add', 'show', 'delete'):
            raise InvalidTransaction('Invalid action: {}'.format(action))
        
        self._action = action
        self._cpf = cpf
        self._name = name

    def to_bytes(self):
        return ",".join([self.action, self.cpf, self.name]).encode()

    @staticmethod
    def from_bytes(payload):
        return ClientPayload(payload=payload)

    @property
    def action(self):
        return self._action

    @property
    def cpf(self):
        return self._cpf

    @property
    def name(self):
        return self._name

main()