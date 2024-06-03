# -*- coding: utf-8 -*-
import requests
import json

def enviar_betinho(mensagem):
    url = "https://evoapi.arsenalsystembr.com.br/message/sendText/ArsenalSystem"
    numero = "88981126816"
    payload = json.dumps({
    "number": numero,
    "options": {
        "delay": 1200,
        "presence": "composing",
        "linkPreview": False
    },
    "textMessage": {
        "text": mensagem
    }
    })
    headers = {
    'Content-Type': 'application/json',
    'apikey': 'z58r8sxtktwnx09hcnng'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.text
