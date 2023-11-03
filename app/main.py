"""A simple HTTP server."""
import socket
from enum import StrEnum, Enum

# Constants
HOST = "localhost"
PORT = 4221
BUFFER_ZISE = 1024
CRLF = "\r\n"
END_HEADERS = CRLF + CRLF


class HttpMethod(StrEnum):
    """An enum representing the HTTP methods."""

    GET = "GET"


class HttpStatusCode(Enum):
    """An enum representing the HTTP status codes."""

    OK = (200, "OK")
    NOT_FOUND = (404, "Not Found")

    def __init__(self, code: int, message: str) -> None:
        self.code = code
        self.message = message


class Response:
    """A class representing a HTTP response."""

    def __init__(self, http_version: str, http_status_code: HttpStatusCode) -> None:
        self.http_version = http_version
        self.http_status_code = http_status_code

    def encode(self) -> bytes:
        """Encode the response into bytes."""
        message = f"{self.http_version} {self.http_status_code.code} {self.http_status_code.message}{END_HEADERS}"
        return message.encode()


class Request:
    """A class representing a HTTP request."""

    def __init__(
        self, http_method: HttpMethod = None, path: str = None, http_version: str = None
    ) -> None:
        self.http_method = http_method
        self.path = path
        self.http_version = http_version

    def decode(self, data: bytes):
        """Parse the data from the client into a Request object."""
        data_list = data.decode().split(CRLF)
        http_method, path, http_version = data_list[0].split()
        self.http_method = HttpMethod(http_method)
        self.path = path
        self.http_version = http_version


def main():
    """The main function."""

    # Create a TCP socket
    server_socket = socket.create_server((HOST, PORT), reuse_port=True)

    # Accept the connection from TCP client
    client_socket, client_address = server_socket.accept()

    with client_socket:
        # Receive the data from client
        data = client_socket.recv(BUFFER_ZISE)

        # Parse the data into a Request object
        request = Request()
        request.decode(data)

        # Create a Response object
        if request.path == "/":
            response = Response(request.http_version, HttpStatusCode.OK)
        else:
            response = Response(request.http_version, HttpStatusCode.NOT_FOUND)

        # Send the response to client
        client_socket.sendall(response.encode())

    # Close the connection
    server_socket.close()


if __name__ == "__main__":
    main()
