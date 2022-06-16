FROM debian:latest

RUN apt-get update && apt-get install curl dnsutils jq git lsb-release python3 python3-pip software-properties-common vim -y

