from http.server import BaseHTTPRequestHandler, SimpleHTTPRequestHandler


class RequestHandler(BaseHTTPRequestHandler):

    def __init__(
        self, forward_fn, add_fn, remove_fn, get_fn, socket, addr, server
    ) -> None:
        self.forward_fn = forward_fn
        self.remove_fn = remove_fn
        self.get_fn = get_fn
        self.add_fn = add_fn
        super().__init__(socket, addr, server)

    def do_GET(self):
        """
        Given the path it either runs or forwards the requests
        """
        # Extracts the URL from the request

        if self.path == "/rep":
            response = self.get_fn()

            return self.handle_GET(response)
        elif self.path == "/add":
            response = self.add_fn()

            return self.handle_GET(response)

        elif self.path == "/rm":
            response = self.remove_fn()

            return self.handle_GET(response)
        else:
            response = self.forward_fn(self.path, self.command)
            return self.handle_GET(response)

    def handle_GET(self, response=b"") -> None:
        """
        Responds to a get request
        """
        if not isinstance(response, bytes):
            response = response.encode()     

        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

        self.wfile.write(response)
