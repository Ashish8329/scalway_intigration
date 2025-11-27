import time
import hmac
import hashlib
import requests
import base64
import uuid
from datetime import datetime
import 

class ScalewayClient:
    

    def __init__(self, access_key, secret_key, project_id):
        self.access_key = access_key
        self.secret_key = secret_key.encode()
        self.project_id = project_id

    def _generate_signature(self, method, path, body=""):
        timestamp = str(int(time.time()))
        content = method + "\n" + path + "\n" + body + "\n" + timestamp
        signature = hmac.new(
            self.secret_key, msg=content.encode(), digestmod=hashlib.sha256
        ).digest()
        signature_b64 = base64.b64encode(signature).decode()

        return signature_b64, timestamp

    def request(self, method, path, body=None, params=None):
        body_str = body if body else ""
        signature, timestamp = self._generate_signature(method, path, body_str)

        headers = {
            "X-Auth-Access-Key": self.access_key,
            "X-Auth-Signature": signature,
            "X-Auth-Timestamp": timestamp,
            "Content-Type": "application/json",
        }

        url = f"{self.BASE_URL}{path}"
        response = requests.request(method, url, headers=headers, json=body, params=params)

        if response.status_code >= 400:
            raise Exception(f"Scaleway API Error: {response.status_code}: {response.text}")

        return response.json()
