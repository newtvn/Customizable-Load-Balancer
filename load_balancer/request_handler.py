from http.server import BaseHTTPRequestHandler, SimpleHTTPRequestHandler
from typing import Callable
from flask import Flask


class RequestHandler:

    def __init__(self, app, forward_fn, add_fn, remove_fn, get_fn) -> None:
        self.app: Flask = app
        self.forward_fn: Callable = forward_fn
        self.remove_fn: Callable = remove_fn
        self.get_fn: Callable = get_fn
        self.add_fn: Callable = add_fn

    
    # def do_GET(self):
    #     """
    #     Given the path it either runs or forwards the requests
    #     """
    #     # Extracts the URL from the request

    #     if self.path == "/rep":
    #         response = self.get_fn()

    #         return self.handle_GET(response)
    #     elif self.path == "/add":
    #         response = self.add_fn()

    #         return self.handle_GET(response)

    #     elif self.path == "/rm":
    #         response = self.remove_fn()

    #         return self.handle_GET(response)
    #     else:
    #         response = self.forward_fn(self.path, self.command)
    #         return self.handle_GET(response)

    # def handle_GET(self, response=b"") -> None:
    #     """
    #     Responds to a get request
    #     """
    #     if not isinstance(response, bytes):
    #         response = response.encode()

    #     self.send_response(200)
    #     self.send_header("Content-type", "application/json")
    #     self.end_headers()

    #     self.wfile.write(response)
