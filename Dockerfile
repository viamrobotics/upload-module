FROM busybox:1.36.1

ARG VIAM_CLI viam-latest-linux-amd64

RUN wget https://storage.googleapis.com/packages.viam.com/apps/viam-cli/$VIAM_CLI
COPY upload.sh .
CMD ./upload.sh
