# System components: LLM response model, knowledge data model
import os
import json

import requests

from gigachat import GigaChat
from gigachat.models import Chat, Messages, MessagesRole

from gigachat import GigaChat

# Get access token for gigachat model

auth_token = os.getenv("gigachat_auth_key")
url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

payload={
  'scope': 'GIGACHAT_API_PERS'
}
headers = {
  'Content-Type': 'application/x-www-form-urlencoded',
  'Accept': 'application/json',
  'RqUID': 'ea92a026-bb76-41a1-bc94-479db56ee8f2',
  'Authorization': 'Basic ' + auth_token
}

response = requests.post(url, headers=headers, data=payload, verify = False)

access_token = response.json()["access_token"]






# GigaChat api access
class LLMModel:
    def __init__(self, access_token = access_token):
        self.access_token = access_token

    def generate(self, text):
        url = "https://api.giga.chat/v1/chat/completions"

        payload={
            "model": "GigaChat-2-Max",
            "messages": [
                {
                    "role": "user",
                    "content": text
                }]}
        headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer ' + self.access_token
        }

        response = requests.request("POST", url, headers=headers, data=json.dumps(payload), verify=False)

        return response.json()["choices"][0]["message"]["content"]
    
llm_model = LLMModel()
llm_response = llm_model.generate("Сколько в тебе параметров?")
print(llm_response)