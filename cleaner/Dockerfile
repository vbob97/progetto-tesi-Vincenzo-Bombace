FROM python:3.7
RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev build-essential
COPY . /cleaner
WORKDIR /cleaner
ENV FLASK_APP=/normalization/consumer.py
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["testApi.py"]