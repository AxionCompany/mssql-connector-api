# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# # Install FreeTDS and other dependencies you might need
RUN apt-get update && apt-get install -y \
    freetds-dev \
    freetds-bin \
    && rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Define environment variable
ENV PORT 9000

EXPOSE $PORT

# run the command to start ugunicorn server, on host 0.0.0.0:9000, 
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app


