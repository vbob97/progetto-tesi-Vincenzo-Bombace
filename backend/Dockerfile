FROM python:3.7
RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev build-essential
COPY . /backend
WORKDIR /backend
ENV FLASK_APP=/backend/backend.py

RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["backend.py"]