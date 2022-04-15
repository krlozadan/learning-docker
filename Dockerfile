# syntax=docker/dockerfile:1

# Every image has to be based on another image
FROM python:3.10

# Sets the working directory of the image so you don't have to specify it every time
WORKDIR /

# Copy files from the host to the image
COPY requirements.txt requirements.txt

# Run commands on the image
RUN pip3 install -r requirements.txt

WORKDIR /app

COPY app .

# Exposes a port and the protocol to be used with it
EXPOSE 5000/tcp

RUN export FLASK_APP=./app/app.py

RUN export FLASK_ENV=development

# Teh command docker will use when starting up the container
CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]