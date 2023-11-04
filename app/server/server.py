"""Server package."""
import socket
import threading

from app.server.constant import BUFFER_ZISE
from app.server.http import Request, HttpMethod, Response, HttpStatusCode
from app.server.log import log_request, print_welcome_message
from app.server.router import Route


class Server:
    """A class representing a HTTP server."""

    def __init__(
        self, host="localhost", port=4221, directory_path=None, thread_pool_size=1
    ):
        self.host = host
        self.port = port
        self.directory_path = directory_path
        self.thread_pool_size = thread_pool_size
        self.routes = []

    def add_route(self, method: HttpMethod, endpoint: str, handler: callable):
        """Add an endpoint to the server."""

        self.routes.append(Route(method, endpoint, handler))

    def handle_request(self, request: Request) -> Response:
        """Route the request to the corresponding handler."""
        for route in self.routes:
            if route.match(request):
                return route.handler(self, request)
        return Response(http_status_code=HttpStatusCode.NOT_FOUND)

    def run(self):
        """Run the server."""
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
            thread.start()

    def server_handler(self, client_socket, client_address):
        """Handle the client connection."""
        # Receive the data from client
        data = client_socket.recv(BUFFER_ZISE)
        # Parse the data into a Request object
        request = Request(data)
        # Create a Response object
        # handle_request
        response = self.handle_request(request)
        # response = router_match(directory_path, request)
        # Send the response to client
        client_socket.sendall(response.encode())
        # Print in log for web server
        log_request(client_address, request, response)
        # Close the connection
        client_socket.close()
