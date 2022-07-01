FROM python:3.10

WORKDIR /app

RUN apt-get update && \
    apt-get install -y freetds-dev

RUN clear
RUN pip install boto3
RUN pip install botocore

ENTRYPOINT ["python"]
