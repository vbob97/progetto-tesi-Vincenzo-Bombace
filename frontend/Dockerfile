FROM python:3.7
RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev build-essential
COPY . /frontend
WORKDIR /frontend
ENV FLASK_APP=/frontend/app.py
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]