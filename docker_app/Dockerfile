FROM python:3.12-alpine
COPY *.py /tmp

RUN apk add curl

EXPOSE 8081
ENTRYPOINT python3 /tmp/server.py -H 0.0.0.0 -p 8081 