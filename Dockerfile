FROM python:3.10.12-slim

RUN apt-get update && apt-get install -qqy wget && apt-get clean && apt autoclean
WORKDIR /usr/bin
RUN wget https://storage.googleapis.com/packages.viam.com/apps/viam-cli/viam-cli-stable-linux-amd64 -q -O viam-amd64
RUN wget https://storage.googleapis.com/packages.viam.com/apps/viam-cli/viam-cli-stable-linux-arm64 -q -O viam-arm64
RUN chmod +x viam-*64
COPY upload.py .

WORKDIR /root
ENTRYPOINT ["upload.py"]
