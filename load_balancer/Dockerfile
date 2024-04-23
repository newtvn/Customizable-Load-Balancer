# Use the Python base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the load balancer project files to the container
COPY . /app

# Install the dependencies
RUN pip install -r requirements.txt

# Add any additional configuration or commands here

# Specify the command to run the load balancer

EXPOSE 5000
CMD [ "python", "core.py" ]
