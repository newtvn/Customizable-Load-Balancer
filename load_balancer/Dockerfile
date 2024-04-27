# Use the Python base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the load balancer project files to the container
COPY ./requirements.txt ./requirements.txt
# Install the dependencies
RUN pip install -r requirements.txt

#Install Docker in the container

RUN apt-get update
RUN apt-get -y install sudo

RUN apt-get -y update
RUN apt-get -y install ca-certificates curl gnupg
RUN install -m 0755 -d /etc/apt/keyrings
RUN curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
RUN chmod a+r /etc/apt/keyrings/docker.gpg

RUN echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
   tee /etc/apt/sources.list.d/docker.list > /dev/null
RUN apt-get -y update

RUN apt-get -y install docker-ce-cli 

ENV USER=theuser
RUN adduser --home /home/$USER --disabled-password --gecos GECOS $USER 
RUN echo "$USER ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/$USER 
RUN chmod 0440 /etc/sudoers.d/$USER 
RUN groupadd docker 
RUN usermod -aG docker $USER 
RUN chsh -s /bin/zsh $USER
USER $USER

ENV HOME=/home/$USER

COPY . /app

# Add any additional configuration or commands here

# Specify the command to run the load balancer
CMD [ "python", "core.py" ]
