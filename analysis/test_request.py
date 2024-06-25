import requests
import re
import json

def extract_server_name(response):
    message = response.get("message", "")
    match = re.search(r'Server: (\w+)', message)
    if match:
        return match.group(1)
    else:
        return None

url = 'http://127.0.0.1:5000/home'

server_count = {}
for i in range(10000):

    response = requests.get(url)
    server_name = extract_server_name(response.json())

    if server_name:
        if server_name in server_count.keys():
            server_count[server_name] += 1
        else:
            server_count[server_name] = 1

print(server_count)
