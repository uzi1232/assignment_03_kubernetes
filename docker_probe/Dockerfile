FROM python:3.12-alpine
COPY *.py /tmp

EXPOSE 30010
ENTRYPOINT python3 /tmp/server.py -H 0.0.0.0 -p 30010