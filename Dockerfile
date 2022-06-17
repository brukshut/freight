FROM python:3.9.10-bullseye

ENV FLASK_APP=freight.py
RUN apt-get update && apt-get install curl jq vim -y && apt-get upgrade -y
RUN pip3 install --upgrade pip
WORKDIR /freight
COPY . /freight
RUN /usr/local/bin/pip install -r requirements.txt
CMD ["/usr/local/bin/python", "-m", "flask", "run", "--host=0.0.0.0"]
