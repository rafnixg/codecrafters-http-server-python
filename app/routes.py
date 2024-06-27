"""Routes module."""

from app.server.http import Request, Response, HttpStatusCode


def upload_files_controller(server, request: Request) -> Response:
    """Upload a file to the server."""
    file_path = request.path.split("/files/")[1]
    with open(f"{server.directory_path}/{file_path}", "w", encoding="UTF-8") as file:
        file.write(request.body)
    return Response(
        http_status_code=HttpStatusCode.CREATED,
    )


def read_files_controller(server, request: Request) -> Response:
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


def user_agent_controller(server, request: Request) -> Response:
    """Return the user agent."""
    return Response(
        body=request.user_agent,
    )


def echo_controller(server, request: Request) -> Response:
    """Return the message."""
    message = request.path.split("/echo/")[1]
    return Response(
        body=message,
        content_encoding=request.accept_encoding if request.accept_encoding else "",
    )


def index_controller(server, request: Request) -> Response:
    """Return the welcome message."""
    return Response()
