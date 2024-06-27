"""Server package."""

import socket
import threading

from app.server.constant import BUFFER_ZISE
from app.server.http import Request, HttpMethod, Response, HttpStatusCode
from app.server.log import log_request
from app.server.utils import print_welcome_message


class Route:
    """A class representing a route."""

    def __init__(self, method: str, path: str, handler: callable):
        self.method = method
        self.path = path
        self.handler = handler

    def match(self, request: Request) -> bool:
        """Check if the route matches the request.
        args:
            request: Request: The HTTP request.
        returns:
            bool: True if the route matches the request, False otherwise.
        """
        match_path = (
            request.path.startswith(self.path[:-1])
            if self.path.endswith("*")
            else (self.path == request.path)
        )
        return self.method == request.http_method and match_path


class Server:
    """A class representing a HTTP server."""

    def __init__(
        self, host="localhost", port=4221, directory_path=None, thread_pool_size=1
    ) -> None:
        self.host = host
        self.port = port
        self.directory_path = directory_path
        self.thread_pool_size = thread_pool_size
        self.routes = []

    def add_route(self, method: HttpMethod, endpoint: str, handler: callable) -> None:
        """Add a route to the server.
        args:
            method: HttpMethod: The HTTP method.
            endpoint: str: The endpoint.
            handler: callable: The handler function.
        returns:
            None
        """

        self.routes.append(Route(method, endpoint, handler))

    def handle_request(self, request: Request) -> Response:
        """Handle the request and return a response.
        args:
            request: Request: The HTTP request.
        returns:
            Response: The HTTP response.
        """
        for route in self.routes:
            if route.match(request):
                return route.handler(self, request)
        return Response(http_status_code=HttpStatusCode.NOT_FOUND)

    def run(self):
        """Run the server."""
        # Create a TCP server socket
        server_socket = socket.create_server((self.host, self.port), reuse_port=True)
        server_socket.listen()
        # Print the welcome message
        print_welcome_message()
        # Keep the server running forever
        while True:
            # Accept the connection from TCP client
            client_socket, client_address = server_socket.accept()
            # Create a thread to handle the client connection
            thread = threading.Thread(
                target=self.server_handler,
                args=(client_socket, client_address),
            )
            # Start the thread
            thread.start()

    def server_handler(self, client_socket, client_address):
        """Handle the client connection.
        args:
            client_socket: socket: The client socket.
            client_address: tuple: The client address.
        returns:
            None
        """
        # Receive the data from client
        data = client_socket.recv(BUFFER_ZISE)
        # Parse the data into a Request object
        request = Request(data)
        # Create a Response object
        response = self.handle_request(request)
        # Send the response to client
        client_socket.sendall(response.encode())
        # Print in log for web server
        log_request(client_address, request, response)
        # Close the connection
        client_socket.close()
