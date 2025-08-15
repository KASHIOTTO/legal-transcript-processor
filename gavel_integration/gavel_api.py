import requests
import os

GAVEL_API_KEY = os.getenv('GAVEL_API_KEY')
BASE_URL = 'https://api.gavel.io/api/documate/v1'

class GavelAPIError(Exception): pass

class GavelClient: 
    def __init__(self, api_key=None):
        slef.api_key = api_key or GAVEL_API_KEY
        if not self.api_key:
            raise GavelAPIError('Missing Gavel API key')

    def submit(self, workflow, variable):
        url = f"{BASE_URL}/interviews/{workflow}/new"
        headers = {'X-API-Key': self.api_key, 'Content-Type': 'application/json'}
        resp = requests.post(url, json={'variables': variables}, headers=headers)
        if not resp.ok:
            raise GavelAPIError(f"Error {resp.status_code}: {resp.text}")
        return resp.json()
