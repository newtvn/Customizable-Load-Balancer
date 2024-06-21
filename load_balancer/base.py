from abc import ABC, abstractmethod
import socket
import threading
import os
import coloredlogs, logging
from request_handler import RequestHandler
from http.server import ThreadingHTTPServer
from typing import Tuple, Dict
import requests
from flask import Flask, jsonify

coloredlogs.install()
logger = logging.getLogger(__name__)


class BaseLoadBalancer(ABC):
    """
    Base Class for Load Balancer
    Override get server to implement load balancing algorithms
    """

    def __init__(self) -> None:
        self.app = Flask("LoadBalancer")

    def get_server(self) -> Tuple[str, int]:
        """
        Returns the server to forward the request to
        """

        return ("127.0.0.1", 4000)

    @abstractmethod
    def get_replicas(self) -> Dict[str, str]:
        """Returns a list of all the replicas"""
        logger.debug("GETTING REPLICAS")

    @abstractmethod
    def add_replica(self) -> Dict[str, str]:
        """Adds a new replica"""
        logger.debug("ADDING REPLICAS")

    @abstractmethod
    def remove_replica(self) -> Dict[str, str]:
        """Removes a replica"""
        logger.debug("REMOVING REPLICA")

    def spawn(self, server_name: str):
        """Spawns a new container with the given server_name and network_name"""
        res = os.popen(
            f"sudo docker run --name {server_name} -d --network=app-networks -e SERVER_ID={server_name} --rm server:latest"
        ).read()

        if len(res) == 0:
            raise Exception("Could not start container")
        else:
            logger.debug("successfully started containerB")

    def kill(self, server_name: str):
        """Kills the container with the given server_name"""

        res = os.popen(f"sudo docker kill {server_name}").read()
        if len(res) == 0:
            raise Exception("Could not stop container")
        else:
            logger.debug("successfully stopped container")

    def run(self, host, port):
        """
        Runs the load balancer
        """
        logger.info(f"LOAD BALANCER IS RUNNING ON {host}:{port}")

        self.handle_routes()
        self.app.run(host=host, port=port)

    def handle_routes(self):
        """
        Handles incoming requests

        """
        self.app.add_url_rule(
            "/rep", "get_replicas", self.get_replicas, methods=["GET"]
        )
        self.app.add_url_rule("/add", "add_replica", self.add_replica, methods=["POST"])
        self.app.add_url_rule(
            "/rm", "remove_replica", self.remove_replica, methods=["DELETE"]
        )
        self.app.add_url_rule("/<path:path>", "forward", self.forward)

    def forward(self, path, method="GET") -> str:
        """
        Forwards request to the address
        """
        server = self.get_server()
        url = f"http://{server[0]}:{server[1]}/{path}"
        response = requests.get(url)
        return response.text
