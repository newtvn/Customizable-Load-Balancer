from abc import ABC, abstractmethod
import socket
import threading
import os
import coloredlogs,logging
from request_handler import RequestHandler
from http.server import ThreadingHTTPServer
from typing import Tuple
import requests

coloredlogs.install()
logger = logging.getLogger(__name__)


class BaseLoadBalancer(ABC):

    def get_server(self):
        """
        returns the server to forward the request to
        """

        return ("127.0.0.1", 4000)

    @abstractmethod
    def forward(self, request):
        # Forwards the request and receives a response back
        pass

    @abstractmethod
    def get_replicas(self):
        """Returns a list of all the replicas"""
        logger.debug("GETTING REPLICAS")

    @abstractmethod
    def add_replica(self):
        """Adds a new replica"""
        logger.debug("ADDING REPLICAS")

    @abstractmethod
    def remove_replica(self):
        """Removes a replica"""
        logger.debug("REMOVING REPLICA")

    def spawn(self, server_name, network_name):
        """Spawns a new container with the given server_name and network_name"""
        res = os.popen(
            f"sudo docker run --name {server_name} --network {network_name} --network-alias {server_name} -d {server_name}:latest -e SERVER_ID={server_name}"
        ).read()

        if len(res) == 0:
            logger.warning("Unable to start container")
        else:
            logger.debug("successfully started containerB")

    def run(self, host, port):
        """
        Runs the load balancer
        """
        logger.info(f"LOAD BALANCER IS RUNNING ON {host}:{port}")
        server = ThreadingHTTPServer((host, port), self.handle_request)
        server.serve_forever()

    def handle_request(self, socket, addr, server):
        """
        Handles incoming requests

        """
        logger.info(f"HANDLING A REQUEST")
        self.handler = RequestHandler(
            forward_fn=self._forward,
            add_fn=self.add_replica,
            remove_fn=self.remove_replica,
            get_fn=self.get_replicas,
            socket=socket,
            addr=addr,
            server=server,
        )

    def _forward(self, path, method="GET"):
        """
        Forwards request to the address
        """

        server = self.get_server()
        url = f"http://{server[0]}:{server[1]}{path}"
        response = requests.get(url)
        return response.text
