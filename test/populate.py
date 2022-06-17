#!/usr/bin/env python

from freight_messages import messages
#from shipments import shipments
import requests
import json

base_url = 'http://localhost:5000'

for msg in messages:
    if msg['type'] == 'ORGANIZATION':
        endpoint = f"{base_url}/organization"
        try:
            response = requests.post(endpoint, json=json.dumps(msg))
            print(response.text)

        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

        print(response.text)

    if msg['type'] == 'SHIPMENT':
        endpoint = f"{base_url}/shipment"
        try:
            response = requests.post(endpoint, json=json.dumps(msg))
            print(response.text)

        except requests.exceptions.RequestException as e:
            raise SystemExit(e)
