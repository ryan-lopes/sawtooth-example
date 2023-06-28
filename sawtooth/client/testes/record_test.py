from dapp import DEFAULT_URL, PIBITIClient

DOCTOR_CPF = '111.111.111-11'
PATIENT_CPF = '222.222.222-22'
CONTROLLER_FAMILY_NAME = 'FAMILY_CONTROLLER'
RECORD_FAMILY_NAME = 'FAMILY_RECORD'
key_file = '/sawtooth/client/jorge.priv'

def record_add():
    rawPayload = {
        "action": "add",
        "patient_cpf": PATIENT_CPF,
        "body": {
            "id_record": "1",
            "title": "Record Title 1",
            "bundle_hash": "BUNDLE_HASH12312312",
        }
    }
    client = PIBITIClient(baseUrl=DEFAULT_URL, keyFile=key_file, family_name=RECORD_FAMILY_NAME, cpf=PATIENT_CPF)
    print("Wrap and send - Add Record")
    response = client._wrap_and_send(rawPayload)
    print("Response: {}".format(response))

def record_show():
    rawPayload = {
        "action": "show",
        "patient_cpf": PATIENT_CPF,
        "body": {
            "id_record": "1",
        }
    }
    client = PIBITIClient(baseUrl=DEFAULT_URL, keyFile=key_file, family_name=RECORD_FAMILY_NAME, cpf=PATIENT_CPF)
    print("Wrap and send - Show Record")
    response = client._wrap_and_send(rawPayload)
    print("Response: {}".format(response))

def record_request():
    rawPayload = {
        "action": "request",
        "patient_cpf": PATIENT_CPF,
        "body": {
            "id_record": "1",
            "doctor_cpf": DOCTOR_CPF, 
            "id_request": "ID_rEQUEST1",
        }
    }
    client = PIBITIClient(baseUrl=DEFAULT_URL, keyFile=key_file, family_name=RECORD_FAMILY_NAME, cpf=PATIENT_CPF)
    print("Wrap and send - Request Record")
    response = client._wrap_and_send(rawPayload)
    print("Response: {}".format(response))

def record_grant():
    rawPayload = {
        "action": "grant",
        "patient_cpf": PATIENT_CPF,
        "body": {
            "id_record": "1",
            "doctor_cpf": DOCTOR_CPF, 
            "id_request": "ID_rEQUEST1",
            "request_status": 1
        }
    }

    client = PIBITIClient(baseUrl=DEFAULT_URL, keyFile=key_file, family_name=RECORD_FAMILY_NAME, cpf=PATIENT_CPF)
    print("Wrap and send - Grant Record")
    response = client._wrap_and_send(rawPayload)
    print("Response: {}".format(response))
