FROM python:3.10.12-slim

RUN apt update && apt install -qqy wget && apt clean && apt autoclean
WORKDIR /usr/bin
RUN wget https://storage.googleapis.com/packages.viam.com/apps/viam-cli/viam-cli-latest-linux-amd64 -q -O viam-amd64
RUN wget https://storage.googleapis.com/packages.viam.com/apps/viam-cli/viam-cli-latest-linux-arm64 -q -O viam-arm64
RUN chmod +x viam
COPY upload.py .

WORKDIR /root
ENTRYPOINT ["upload.py"]
