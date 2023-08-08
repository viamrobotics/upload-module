FROM python:3.10.12-slim

ARG VIAM_CLI=viam-latest-linux-amd64

RUN apt update && apt install -qqy wget && apt clean && apt autoclean
WORKDIR /usr/bin
RUN wget https://storage.googleapis.com/packages.viam.com/apps/viam-cli/$VIAM_CLI -q -O viam
RUN chmod +x viam
COPY upload.py .

WORKDIR /root
ENTRYPOINT ["upload.py"]
