import hashlib
import base64
import random
import requests
import yaml
import json

from sawtooth_signing import create_context
from sawtooth_signing import CryptoFactory
from sawtooth_signing import ParseError
from sawtooth_signing.secp256k1 import Secp256k1PrivateKey

from sawtooth_sdk.protobuf.transaction_pb2 import TransactionHeader
from sawtooth_sdk.protobuf.transaction_pb2 import Transaction
from sawtooth_sdk.protobuf.batch_pb2 import BatchList
from sawtooth_sdk.protobuf.batch_pb2 import BatchHeader
from sawtooth_sdk.protobuf.batch_pb2 import Batch

DEFAULT_URL = 'http://rest-api:8008'

def _hash(data):
    return hashlib.sha512(data).hexdigest()

class PIBITIClient(object):

    _baseUrl = None
    _signer = None
    _publicKey = None
    _family_name = None
    _cpf = None
    def __init__(self, baseUrl, keyFile=None, family_name=None, cpf=None):
        if family_name is None:
            raise Exception('Family name is N')
        if cpf is None:
            raise Exception('Cpf is None')

        self._family_name = family_name
        self._cpf = cpf    
        self._baseUrl = baseUrl

        if keyFile is None:
            self._signer = None
            return

        try:
            with open(keyFile) as fd:
                privateKeyStr = fd.read().strip()
        except OSError as err:
            raise Exception('Failed to read private key {}: {}'.format(
                keyFile, str(err)))

        try:
            privateKey = Secp256k1PrivateKey.from_hex(privateKeyStr)
        except ParseError as err:
            raise Exception('Failed to load private key: {}'.format(str(err)))

        self._signer = CryptoFactory(create_context('secp256k1')).new_signer(privateKey)

        self._publicKey = self._signer.get_public_key().as_hex()

        self._address = _hash(self._family_name.encode('utf-8'))[0:6] + _hash(self._cpf.encode('utf-8'))[0:64]
 
    def _send_to_restapi(self,suffix,data=None,contentType=None):

        if self._baseUrl.startswith("http://"):
            url = "{}/{}".format(self._baseUrl, suffix)
        else:
            url = "http://{}/{}".format(self._baseUrl, suffix)

        headers = {}

        if contentType is not None:
            headers['Content-Type'] = contentType

        try:
            if data is not None:
                result = requests.post(url, headers=headers, data=data)
            else:
                result = requests.get(url, headers=headers)

            if not result.ok:
                raise Exception("Error {}: {}".format(
                    result.status_code, result.reason))

        except requests.ConnectionError as err:
            raise Exception(
                'Failed to connect to {}: {}'.format(url, str(err)))

        except BaseException as err:
            raise Exception(err)

        return result.text


    def _wrap_and_send(self, data):
        payload = json.dumps(data).encode()

        # Construct the address where we'll store our state
        address = self._address
        inputAddressList = [address]
        outputAddressList = [address]

        # Create a TransactionHeader
        header = TransactionHeader(
            signer_public_key=self._publicKey,
            family_name=self._family_name,
            family_version="1.0",
            inputs=inputAddressList,
            outputs=outputAddressList,
            dependencies=[],
            payload_sha512=_hash(payload),
            batcher_public_key=self._publicKey,
            nonce=random.random().hex().encode()
        ).SerializeToString()

        # Create a Transaction from the header and payload above
        transaction = Transaction(
            header=header,
            payload=payload,
            header_signature=self._signer.sign(header)
        )

        transactionList = [transaction]

        # Create a BatchHeader from transactionList above
        header = BatchHeader(
            signer_public_key=self._publicKey,
            transaction_ids=[txn.header_signature for txn in transactionList]
        ).SerializeToString()

        #Create Batch using the BatchHeader and transactionList above
        batch = Batch(
            header=header,
            transactions=transactionList,
            header_signature=self._signer.sign(header))

        #Create a Batch List from Batch above
        batch_list = BatchList(batches=[batch])

        # Send batch_list to rest-api
        return self._send_to_restapi(
            "batches",
            batch_list.SerializeToString(),
            'application/octet-stream')

def main():

    FAMILY_NAME = 'FAMILY_CONTROLLER'
    CPF = '000.000.000-21'
    rawPayload = {
        "action": "add",
        "type": "doctor",
        "body": {
            "cpf": CPF,
            "name": "ryan",
        }
    }
    
    key_file = '/sawtooth/client/jorge.priv'
    client = PIBITIClient(baseUrl=DEFAULT_URL, keyFile=key_file, family_name=FAMILY_NAME, cpf=CPF)
    print("Wrap and send")
    response = client._wrap_and_send(rawPayload)
    print("Response: {}".format(response))

main()

# Funções para o contrato
## ControllerSC
### addPacient
### deletePacient
### showPacient
### addDoctor
### deleteDoctor
### showDoctor
