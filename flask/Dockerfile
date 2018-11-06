FROM ubuntu:trusty

RUN apt-get update && \
    apt-get install -y python-pip curl zip

RUN pip install flake8

WORKDIR /app

EXPOSE 80

COPY . /app

RUN chmod +x /app/run.sh

CMD ["/app/run.sh"]
