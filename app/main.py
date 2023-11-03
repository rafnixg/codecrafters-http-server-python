"""A simple HTTP server."""
import argparse
import socket
import threading
import datetime

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

    def __init__(
        self,
        http_version: str,
        http_status_code: HttpStatusCode,
        content_type="text/plain",
        body: str = None,
    ) -> None:
        self.http_version = http_version
        self.http_status_code = http_status_code
        self.body = body
        self.content_type = content_type
        self.content_length = 0 if self.body is None else len(self.body)

    def encode(self) -> bytes:
        """Encode the response into bytes."""
        message = f"{self.http_version} {self.http_status_code.code} {self.http_status_code.message}{CRLF}"
        message += f"Content-Type: {self.content_type}{CRLF}"
        message += f"Content-Length: {self.content_length}{END_HEADERS}"
        message += f"{self.body}"
        return message.encode()


class Request:
    """A class representing a HTTP request."""

    def __init__(
        self, http_method: HttpMethod = None, path: str = None, http_version: str = None
    ) -> None:
        self.http_method = http_method
        self.path = path
        self.http_version = http_version
        self.user_agent = None

    def extract_http_method(self, data_list: list):
        """Extract the HTTP method from the data."""
        return data_list[0].split()

    def extract_user_agent(self, data_list: list):
        """Extract the user agent from the data."""
        user_agent = data_list[2]
        if user_agent:
            user_agent = user_agent.split(":")[1].strip()
        return user_agent

    def decode(self, data: bytes):
        """Parse the data from the client into a Request object."""
        data_list = data.decode().split(CRLF)
        http_method, self.path, self.http_version = self.extract_http_method(data_list)
        self.user_agent = self.extract_user_agent(data_list)
        self.http_method = HttpMethod(http_method)


def log_request(client_address, request: Request, response: Response):
    """Print the request in log."""
    date_time = datetime.datetime.now()
    date_time_format = date_time.strftime("%d/%m/%Y %H:%M:%S")
    print(
        f"[{date_time_format}] {response.http_status_code.code} {request.http_method} {request.path} {client_address[0]} - {client_address[1]} - {request.user_agent}"
    )


def router(directory_path: str, request: Request) -> Response:
    """Route the request to the corresponding handler."""
    response = Response(
        http_version=request.http_version,
        http_status_code=HttpStatusCode.NOT_FOUND
    )
    # Create a Response object
    if request.path == "/":
        response = Response(
            http_version=request.http_version,
            http_status_code=HttpStatusCode.OK
        )
    elif request.path.startswith("/echo/"):
        message = request.path.split("/echo/")[1]
        response = Response(
            http_version=request.http_version,
            http_status_code=HttpStatusCode.OK,
            body=message,
        )
    elif request.path.startswith("/user-agent"):
        response = Response(
            http_version=request.http_version,
            http_status_code=HttpStatusCode.OK,
            body=request.user_agent,
        )
    elif request.path.startswith("/files/"):
        file_path = request.path.split("/files/")[1]
        try:
            with open(f"{directory_path}/{file_path}", "r", encoding="UTF-8") as file:
                response = Response(
                    http_version=request.http_version,
                    http_status_code=HttpStatusCode.OK,
                    content_type="application/octet-stream",
                    body=file.read(),
                )
        except FileNotFoundError:
            response = Response(request.http_version, HttpStatusCode.NOT_FOUND)
    return response


def client_handler(client_socket, client_address, directory_path):
    """Handle the client connection."""
    # Receive the data from client
    data = client_socket.recv(BUFFER_ZISE)
    # Parse the data into a Request object
    request = Request()
    request.decode(data)
    # Create a Response object
    response = router(directory_path, request)
    # Send the response to client
    client_socket.sendall(response.encode())
    # Print in log for web server
    log_request(client_address, request, response)
    # Close the connection
    client_socket.close()


def print_welcome_message():
    """Print the welcome message."""
    print(f"Listening on {HOST}:{PORT}...")
    print("Press Ctrl+C to quit.\n")
    print("Available endpoints:")
    print("GET /")
    print("GET /echo/<message>")
    print("GET /user-agent")


def get_directory_path():
    """Get the directory path from the command line arguments.
    --directory <directory_path>
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--directory", help="the directory path")
    args = parser.parse_args()
    if not args.directory:
        parser.error("Please specify the directory path.")
    return args.directory


def main():
    """The main function."""
    # Get the directory path from the command line arguments
    directory_path = get_directory_path()

    # Create a TCP socket
    server_socket = socket.create_server((HOST, PORT), reuse_port=True)
    server_socket.listen()
    print_welcome_message()

    while True:
        # Accept the connection from TCP client
        client_socket, client_address = server_socket.accept()
        # Create a thread to handle the client connection
        thread = threading.Thread(
            target=client_handler, args=(client_socket, client_address, directory_path)
        )
        thread.start()


if __name__ == "__main__":
    main()
