"""Router module."""
from app.server.http import Request, Response, HttpStatusCode


class Route:
    """A class representing a route."""

    def __init__(self, method: str, path: str, handler: callable):
        self.method = method
        self.path = path
        self.handler = handler

    def match(self, request: Request) -> bool:
        """Check if the route matches the request."""
        match_path = (
            request.path.startswith(self.path[:-1])
            if self.path.endswith("*")
            else (self.path == request.path)
        )
        return self.method == request.http_method and match_path


# Controllers


def upload_files_handler(server, request: Request) -> Response:
    """Upload a file to the server."""
    file_path = request.path.split("/files/")[1]
    with open(f"{server.directory_path}/{file_path}", "w", encoding="UTF-8") as file:
        file.write(request.body)
    return Response(
        http_status_code=HttpStatusCode.CREATED,
    )


def read_files_handler(server, request: Request) -> Response:
    """Read a file from the server."""
    try:
        file_path = request.path.split("/files/")[1]
        with open(
            f"{server.directory_path}/{file_path}", "r", encoding="UTF-8"
        ) as file:
            return Response(
                content_type="application/octet-stream",
                body=file.read(),
            )
    except FileNotFoundError:
        return Response(http_status_code=HttpStatusCode.NOT_FOUND)


def user_agent_handler(server, request: Request) -> Response:
    """Return the user agent."""
    return Response(
        body=request.user_agent,
    )


def echo_handler(server, request: Request) -> Response:
    """Return the message."""
    message = request.path.split("/echo/")[1]
    return Response(
        body=message,
        content_encoding=request.accept_encoding if request.accept_encoding else '',
    )


def index_handler(server, request: Request) -> Response:
    """Return the welcome message."""
    return Response()


# def router_match(directory_path: str, request: Request) -> Response:
#     """Route the request to the corresponding handler."""
#     response = Response(http_status_code=HttpStatusCode.NOT_FOUND)
#     # Create a Response object
#     if request.path == "/":
#         response = index_handler()
#     elif request.path.startswith("/echo/"):
#         response =  echo_handler(request)
#     elif request.path.startswith("/user-agent"):
#         response =  user_agent_handler(request)
#     elif (
#         request.path.startswith("/files/")
#         and directory_path
#         and request.http_method == HttpMethod.GET
#     ):
#         response = read_files_handler(directory_path, request)
#     elif (
#         request.path.startswith("/files/")
#         and directory_path
#         and request.http_method == HttpMethod.POST
#     ):
#         response = upload_files_handler(directory_path, request)
#     return response
