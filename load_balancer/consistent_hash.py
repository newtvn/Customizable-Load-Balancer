from random import randint

class ConsistentHash:
    
    slots : int = 512
    num_virtual_servers :  int 
    servers : dict[int , str]
    hashmap : list[any]


    
    def __init__(self):
        self.slots = 512
        self.num_virtual_servers = 9
        self.hashmap = [None] * self.slots
        self.servers = {}

    def request_hash(self, i : int ) -> int:
        return ((i**2) + (2*i) + 17 ) % self.slots

    def server_hash(self, i : int, j : int) -> int:
        return ((i**2)+(j**2)+(2*j)+ 25) % self.slots

    def generate_server_id(self, server_name : str) -> int:
        while True:
            id =  randint(1000, 9999)
            if id not in self.servers:
                self.servers[id] = server_name
                return id

    def get_server_id(self, server_name : str) -> int:
        return list(self.servers.keys())[list(self.servers.values()).index(server_name)]

    def add_server(self, server_name : str) -> int:
        server_id = self.generate_server_id(server_name)
        for j in range(self.num_virtual_servers) :
            position = self.server_hash(server_id,j)
            if self.hashmap[position] is None:
                self.hashmap[position] = {'server' : server_id} 
            else:
                while self.hashmap[position] is not None:
                    position = (position + 1) % self.slots
                    if self.hashmap[position] is None:
                        self.hashmap[position] = {'server' : server_id}
        return server_id

                        

    
    def remove_server(self,server_name : str):
        if server_name not in self.servers.values():
            return False

        for pos in range(self.slots):
            if self.hashmap[pos] is None:
                continue
            if 'server' in self.hashmap[pos]:
                if self.hashmap[pos]['server'] == self.get_server_id(server_name) :
                    self.hashmap[pos] = None
        return True
    
    def add_request(self, request_id : int) -> str:
        position = self.request_hash(request_id)
        if self.hashmap[position] is None:
            pass
        else:
            while 'server' in self.hashmap[position]:
                position = (position + 1) % self.slots
        self.hashmap[position] = {'request' : request_id} 
        count = 0
        while count < self.slots:
            if self.hashmap[position] is None:
                position = (position + 1) % self.slots
            elif 'server' not in self.hashmap[position]:
                position = (position + 1) % self.slots
            else :
                return self.servers[self.hashmap[position]['server']]

            count = count + 1
        return False
                

    def print_map(self):
        for slot in self.hashmap:
            print(f'{slot}')

        
    