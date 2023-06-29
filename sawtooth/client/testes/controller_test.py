from dapp import DEFAULT_URL, PIBITIClient
from testes.config_test import *


def doctor_add():
    rawPayload = {
        "action": "add",
        "type": "doctor",
        "body": {
            "cpf": DOCTOR_CPF,
            "name": "ryan",
        }
    }
    client = PIBITIClient(baseUrl=DEFAULT_URL, keyFile=key_file, family_name=CONTROLLER_FAMILY_NAME, cpf=DOCTOR_CPF)
    print("Wrap and send - Add Doctor")
    response = client._wrap_and_send(rawPayload)
    print("Response: {}".format(response))

def patient_add():
    rawPayload = {
        "action": "add",
        "type": "patient",
        "body": {
            "cpf": PATIENT_CPF,
            "name": "ryan",
        }
    }
    client = PIBITIClient(baseUrl=DEFAULT_URL, keyFile=key_file, family_name=CONTROLLER_FAMILY_NAME, cpf=PATIENT_CPF)
    print("Wrap and send - Add Patient")
    response = client._wrap_and_send(rawPayload)
    print("Response: {}".format(response))

def patient_show():
    rawPayload = {
        "action": "show",
        "type": "patient",
        "body": {
            "cpf": PATIENT_CPF,
            "name": "A"
        }
    }
    client = PIBITIClient(baseUrl=DEFAULT_URL, keyFile=key_file, family_name=CONTROLLER_FAMILY_NAME, cpf=PATIENT_CPF)
    print("Wrap and send - show Patient")
    response = client._wrap_and_send(rawPayload)
    print("Response: {}".format(response))

