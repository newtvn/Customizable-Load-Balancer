# Customizable Load Balancer 

## Project Overview 

Load balancers are critical for managing multiple server replicas in distributed systems and ensuring that client requests are distributed evenly across servers. This project involves the following tasks:

1. **Server Implementation**: Create a simple web server that handles HTTP requests.
2. **Consistent Hashing**: Develop a consistent hashing mechanism to distribute load effectively.
3. **Load Balancer Implementation**: Implement a load balancer that uses consistent hashing to manage server replicas.
4. **Performance Analysis**: Test the performance of the load balancer.

The primary goal is to develop a scalable and fault-tolerant system that maintains a consistent load distribution even as server instances are dynamically added or removed.

## Installation Instructions
### Prerequisites

Ensure that you have the following software installed on your system:

- **Docker**: Version 20.10.23 or higher  ([How to install Docker](https://www.docker.com/get-started/))
- **Python**: Python 3.0 or higher
- **Make** (Optional)

### Steps 

1. **Clone the Repository**

  ```bash
   git clone https://github.com/newtvn/Customizable-load-balancer.git
   cd Customizable-load-balancer
```
2. **Build Server Docker Image**


  ```bash
   docker build -t server:latest server/
```

3. **Deploy the System using Docker Compose**


  ```bash
   docker compose up
```

or you can use the included makefile by running:

  ```bash
   make run
```
## Usage Guidelines

Once the system is up and running, you can interact with the load balancer using the following endpoints:

- **GET /home**: Retrieves a message from a server replica.
- **GET /heartbeat**: Sends a heartbeat response to check the server status.
- **GET /rep**: Returns the status of the replicas managed by the load balancer.
- **POST /add**: Adds new server instances to the load balancer.

    This endpoints accepts a JSON payload defining the number of server instances being added and their names as below:
  ```json
    {"n": 2, "hostnames": ["Server4", "Server5"]}
   =```
- **DELETE /rm**: Removes server instances from the load balancer.

### Example Requests

**Get Server Message**
  ```bash
     curl http://localhost:5000/home
```
**Add New Server Instances**
  ```bash
     curl -X POST -H "Content-Type: application/json" -d '{"n": 2, "hostnames": ["Server4", "Server5"]}' http://localhost:5000/add
```

**Remove Server Instances**
  ```bash
     curl -X DELETE -H "Content-Type: application/json" -d '{"n": 1, "hostnames": ["Server4"]}' http://localhost:5000/rm
```
## Testing

### Running Tests
The Load Balancer tests are stored in the ` tests\` directory and can be run by excecuting:

  ```bash
pytest tests/test.py
```
## Performance Analysis

### Experiment 1: Load Distribution

- Launch 10,000 asynchronous requests on 3 server containers.
- Record the number of requests handled by each server and plot a bar chart.
- Expected Outcome: Even distribution of load among server instances.

![image](https://github.com/nguthiru/Customizable-load-balancer/assets/65071563/4dd71147-b598-42a7-94d0-7633673374da)



### Experiment 2: Scalability

- Increment the number of server containers from 2 to 6 (launching 10,000 requests each time).
- Plot a line chart showing the average load of the servers at each run.
- Expected Outcome: Efficient scaling with even load distribution as server instances increase.
![image](https://github.com/nguthiru/Customizable-load-balancer/assets/65071563/23d841b0-bdba-46a0-8081-cbdeffd12231)


### Experiment 3: Failure Recovery

- Test load balancer endpoints and simulate server failures.
- Ensure the load balancer spawns new instances to handle the load and maintain the specified number of replicas.
#### Results
![image](https://github.com/nguthiru/Customizable-load-balancer/assets/65071563/ea80a5f6-2081-45c9-b1f2-7c91d355efb7)
<br>
<sup>Containers  with the prefix 'emergency_' are spawned on failure of a replica.</sup>
- On failure of 'S2' and 'S4' replica 'emergency_58' and 'emergency_43' are spawned

### Experiment 4: Hash Function Modification

- Modified the hash function: i % 512(number) of slots.
- Repeat experiments 1 and 2, analyzing the impact on load distribution and scalability.
- #### Experiment 1 Results:
  ![image](https://github.com/nguthiru/Customizable-load-balancer/assets/65071563/37fe90b7-d576-4410-a0a6-e067ff4d67d2)
- #### Experiment 2 Results:
  ![image](https://github.com/nguthiru/Customizable-load-balancer/assets/65071563/2fd094d2-4883-4b0d-a732-06be19a3ee14)


