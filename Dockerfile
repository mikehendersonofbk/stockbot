FROM python:3.8

RUN mkdir -p /opt
WORKDIR /opt
COPY . .
RUN pip install -r requirements.txt
CMD tail -f /dev/null