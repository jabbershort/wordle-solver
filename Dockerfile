FROM ubuntu:focal

SHELL ["/bin/bash","-c"]

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python-dev

ADD requirements.txt /requirements.txt

RUN python3 -m pip install -r requirements.txt

ADD src/ /app/

CMD python3 /app/flask_app.py
