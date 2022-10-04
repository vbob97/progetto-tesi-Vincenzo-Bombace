FROM python:3.7
RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev build-essential
COPY . /visualizer
WORKDIR /visualizer
ENV FLASK_APP=/visualizer/app.py
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]