FROM ubuntu:22.04

ARG VIAM_CLI=viam-latest-linux-amd64

RUN apt update && apt install -qqy wget && apt clean && apt autoclean
RUN wget https://storage.googleapis.com/packages.viam.com/apps/viam-cli/$VIAM_CLI
COPY upload.sh .

CMD ./upload.sh
