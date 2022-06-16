#!/bin/bash

##
## use this script to run the flask application locally
##
source venv/bin/activate
export FLASK_APP=freight.py
export FLASK_DEBUG=1
flask run --host 0.0.0.0
