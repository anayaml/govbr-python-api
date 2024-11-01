from fastapi import HTTPException
import requests
from datetime import datetime, timedelta
import base64
import json

SERVER_URL = 'https://h-apigateway.conectagov.estaleiro.serpro.gov.br'
TOKEN_REQUEST_URL = SERVER_URL + '/oauth2/jwt-token'
CLIENT_ID = '8ddc46f2-f6a3-4077-9e04-74b55de934a5'
CLIENT_SECRET = '06d4aaac-1412-45f6-bd7c-38b2bef0d706'
CONSULTA_CPF_URL = SERVER_URL + '/api-cpf-light/v2/consulta/cpf'

EXPIRATION_WINDOW_IN_SECONDS = 300

token_storage = None
token_expiry = None

def extract_exp(token):
    payload = token.split('.')[1]
    padding = len(payload) % 4
    if padding:
        payload += '=' * (4 - padding)
    decoded = base64.b64decode(payload)
    exp = json.loads(decoded)['exp']
    return exp

def get_token():
    global token_storage, token_expiry
    auth = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f'Basic {auth}'
    }
    data = 'grant_type=client_credentials'
    response = requests.post(TOKEN_REQUEST_URL, headers=headers, data=data)
    response.raise_for_status()
    token_storage = response.json()['access_token']
    exp_timestamp = extract_exp(token_storage)
    token_expiry = datetime.fromtimestamp(exp_timestamp)

def get_consulta_cpf(token):
    headers = {
        'Content-Type': 'application/json',
        'x-cpf-usuario': '77689062768',
        'Authorization': f'Bearer {token}'
    }
    data = json.dumps({
        "listaCpf": ["00045024936", "26616776824", "82272182100"]
    })
    response = requests.post(CONSULTA_CPF_URL, headers=headers, data=data)
    response.raise_for_status()
    return response.json()

def consulta_cpf():
    global token_storage, token_expiry
    if token_storage is None or datetime.now() >= (token_expiry - timedelta(seconds=EXPIRATION_WINDOW_IN_SECONDS)):
        try:
            get_token()
        except requests.RequestException as e:
            raise HTTPException(status_code=500, detail=f"Error obtaining token: {e}")
    try:
        lista_cpf = get_consulta_cpf(token_storage)
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error querying CPF API: {e}")

    return lista_cpf

print(consulta_cpf())