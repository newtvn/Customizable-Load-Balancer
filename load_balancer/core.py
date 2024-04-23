from base import BaseLoadBalancer
from parsers import response_parser
import http.server
class LoadBalancer(BaseLoadBalancer):

    def forward(self, request):
        """
        Forwards the request to a backend server and returns response

        The server address is got using consistent hashing
        """
        return self._forward(address=("127.0.0.1",4000))
    def spawn(self, server_name):
        return super().spawn(server_name)
    
    def get_replicas(self):
        return response_parser({"replicas": ["server1", "server2"]})
    
    def add_replica(self):
        return response_parser("ADDED IT")
    
    def remove_replica(self):
        return response_parser("REMOVING REPLICA")
        
        



load_balancer = LoadBalancer()

load_balancer.run(host="127.0.0.1", port=5000)

