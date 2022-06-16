#!/usr/bin/env python

from freight_messages import messages
#from shipments import shipments
import requests
import json

url = 'http://localhost:5000'

for msg in messages:
    if msg['type'] == 'ORGANIZATION':
        endpoint = f"http://localhost:5000/organization"
        response = requests.post(endpoint, json=json.dumps(msg))
        print(response.text)

    if msg['type'] == 'SHIPMENT':
        print(json.dumps(msg))
        endpoint = f"http://localhost:5000/shipment"
        response = requests.post(endpoint, json=json.dumps(msg))
        print(response.text)

