FROM python:3.9-slim-buster

RUN apt-get update && apt-get install curl jq vim -y && apt-get upgrade -y
RUN pip3 install --upgrade pip

ENV FLASK_APP=freight.py
WORKDIR /freight
COPY . /freight
RUN /usr/local/bin/pip install -r requirements.txt

CMD ["/usr/local/bin/python", "-m", "flask", "run", "--host=0.0.0.0"]
