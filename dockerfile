# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# # Install FreeTDS and other dependencies you might need
# RUN apt-get update && apt-get install -y \
#     freetds-dev \
#     freetds-bin \
#     && rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 9000 available to the world outside this container
EXPOSE 9000

# Define environment variable

# Run app.py when the container launches
CMD ["python", "./main.py"]
