# Familias de transação

## Controller family

### add/show/delete:
``` json
        "action": "(add/show/delete)",
        "type": "(doctor/patient)",
        "body": {
            "cpf": (DOCTOR_CPF/PATIENT_CPF),
            "name": "Name",
        }
```

## Record family

### add
```json
        "action": "add",
        "patient_cpf": PATIENT_CPF,
        "body": {
            "id_record": "record_id",
            "title": "record_title",
            "bundle_hash": "BUNDLE_HASH",
        }
```
### show/delete
```json
        "action": "(show/delete)",
        "patient_cpf": PATIENT_CPF,
        "body": {
            "id_record": "record_id",
        }
```

### request 
```json
        "action": "request",
        "patient_cpf": PATIENT_CPF,
        "body": {
            "id_record": "record_id",
            "doctor_cpf": DOCTOR_CPF, 
            "id_request": "ID_REQUEST",
        }
```
### grant
```json
        "action": "grant",
        "patient_cpf": PATIENT_CPF,
        "body": {
            "id_record": "1",
            "doctor_cpf": DOCTOR_CPF, 
            "id_request": "ID_REQUEST",
            "request_status": 1
        }
```
## TODO

- [] Verificar campos opcionais no payload.
- [] Corrigir a questao do tipo de usuario no registro de record (Doctor com records).
- [] Corrigir show e delete do controller.
- [] Tratar records e request com id repetidos.
- [] Tratamentos de exceptions.
