from typing import Tuple
from base import BaseLoadBalancer
from parsers import response_parser
import http.server
from consistent_hash import ConsistentHash
from flask import request
import threading
import random


class LoadBalancer(BaseLoadBalancer):

    def __init__(self):
        self.consistent_hash = ConsistentHash()
        self.replicas = set()
        super().__init__()

    def get_server(self) -> Tuple[str, int]:
        """
        Returns the server to forward the request to
        """
        request_id = random.randint(1000, 9999)
        server = self.consistent_hash.add_request(request_id)
        self.consistent_hash.complete_request(request_id)
        return server, 4000

    def get_replicas(self):
        """
        Returns the replicas in the load balancer

        """

        response = {
            "message": {"N": len(self.replicas), "replicas": list(self.replicas)},
            "status": "success",
        }
        return response_parser(response)

    def add_replica(self, *args, **kwargs):
        """

        Adds a new replica to the load balancer
        """
        if request.method == "POST":
            data = request.json
            n = data.get("n", 1)
            hostnames = data.get("hostnames", [])
            if len(hostnames) != n:
                return response_parser(
                    "Number of hostnames do not match the number of replicas", 400
                )
            else:
                for hostname in hostnames:
                    if hostname in self.replicas:
                        return response_parser(
                            f"{hostname} already in the replicas", 400
                        )
                    try:
                        threading.Thread(
                            target=self.handle_add, args=(hostname,)
                        ).start()
                    except Exception as e:
                        return response_parser(str(e), 500)
            return self.get_replicas()

    def handle_add(self, hostname):
        try:
            self.spawn(hostname)
            self.replicas.add(hostname)
            self.consistent_hash.add_server(hostname)
            print(f"Added {hostname} to the replicas")
        except Exception as e:
            return response_parser(str(e), 500)

    def remove_replica(self):
        """
        Removes a replica from the load balancer
        """
        if request.method == "DELETE":
            data = request.json
            hostnames = data.get("hostnames")
            n = data.get("n", 1)
            if len(hostnames) != n:
                return response_parser(
                    "Number of hostnames do not match the number of replicas", 400
                )
            else:
                for hostname in hostnames:
                    if hostname in self.replicas:
                        try:
                            threading.Thread(
                                target=self.handle_remove, args=(hostname,)
                            ).start()
                        except Exception as e:
                            return response_parser(str(e), 500)
                    else:
                        return response_parser(f"{hostname} not in the replicas", 400)
                return self.get_replicas()

    def handle_remove(self, hostname):
        try:
            self.kill(hostname)
            self.replicas.remove(hostname)
            self.consistent_hash.remove_server(hostname)
            print(f"Removed {hostname} from the replicas")
        except Exception as e:
            return response_parser(str(e), 500)


load_balancer = LoadBalancer()

load_balancer.run(host="127.0.0.1", port=5000)
