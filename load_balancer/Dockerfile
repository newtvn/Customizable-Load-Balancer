# Use the Python base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the load balancer project files to the container
COPY ./requirements.txt ./requirements.txt
# Install the dependencies
RUN pip install -r requirements.txt

COPY . /app

# Add any additional configuration or commands here

# Specify the command to run the load balancer
CMD [ "python", "core.py" ]
