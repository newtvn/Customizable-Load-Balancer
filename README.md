# Customizable Load Balancer in Docker

This document outlines a project to implement a customizable load balancer using Docker.

## Overview

This project involves building a load balancer that efficiently distributes requests among multiple server replicas using consistent hashing. It automatically manages the number of replicas, scaling up by spawning new instances in case of server failures. Docker containerization simplifies deployment and management.

## Purpose

The load balancer aims to handle increasing client loads by efficiently distributing requests across server replicas. This improves resource utilization and throughput in applications like distributed caching, databases, and network traffic systems.

## Coding Environment

- **OS**: Ubuntu 20.04 LTS or above
- **Docker**: Version 20.10.23 or above
- **Languages**: Python (preferred), C++, Java, or your choice

## Installation

1. **Install Docker:**

```bash
sudo apt-get update
sudo apt-get install ca-certificates curl gnupg lsb-release
sudo mkdir -p /etc/apt/keyrings
curl -fsSL [https://download.docker.com/linux/ubuntu/gpg](https://download.docker.com/linux/ubuntu/gpg) | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] [https://download.docker.com/linux/ubuntu](https://download.docker.com/linux/ubuntu) $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io
```

2. **Install Docker-Compose:**

```bash
sudo curl -SL https://github.com/docker/compose/releases/download/v2.15.1/docker-compose-linux-x86_64 -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
```

## How to Use

1. **Running the Project:**
   - Clone the repository:
     ```bash
git clone <repository-url>
cd <repository-directory>
```

   - Build and start containers:
```bash
docker-compose up --build
```

2. **Interacting with the Load Balancer:**
   - Check replica status:
     ```bash
curl -X GET http://localhost:5000/rep
```
   - Add new server instances:
```bash
curl -X POST -H "Content-Type: application/json" -d '{"n": 2, "hostnames": ["S4", "S5"]}' http://localhost:5000/add
```
   - Remove server instances:
     ```bash
curl -X DELETE -H "Content-Type: application/json" -d '{"n": 2, "hostnames": ["S4", "S5"]}' http://localhost:5000/rm
```
   - Route requests through the load balancer:
```bash
curl -X GET http://localhost:5000/home
```
## Dependancies

-Docker
-Docker-Compose

## Design Choices and Assumptions

- **Consistent Hashing**: Ensures even load distribution and handles dynamic server changes with minimal disruption.
- **Docker**: Provides an isolated and reproducible environment.
- **HTTP Endpoints**: Simplifies communication between clients, the load balancer, and server replicas.

## Testing and Performance Analysis

### Experiment 1: Load Distribution

- Launch 10,000 asynchronous requests on 3 server containers.
- Record the number of requests handled by each server and plot a bar chart.
- Expected Outcome: Even distribution of load among server instances.

![image](https://github.com/nguthiru/Customizable-load-balancer/assets/65071563/4dd71147-b598-42a7-94d0-7633673374da)



### Experiment 2: Scalability

- Increment the number of server containers from 2 to 6 (launching 10,000 requests each time).
- Plot a line chart showing the average load of the servers at each run.
- Expected Outcome: Efficient scaling with even load distribution as server instances increase.
![image](https://github.com/nguthiru/Customizable-load-balancer/assets/65071563/f36cf317-fe30-4c7e-805d-2522dda22769)


### Experiment 3: Failure Recovery

- Test load balancer endpoints and simulate server failures.
- Ensure the load balancer spawns new instances to handle the load and maintain the specified number of replicas.

### Experiment 4: Hash Function Modification

- Modify the hash functions H(i) and Φ(i,j).
- Repeat experiments 1 and 2, analyzing the impact on load distribution and scalability.
