"""Router module."""
from app.server.http import Request, Response, HttpStatusCode, HttpMethod


def router(directory_path: str, request: Request) -> Response:
    """Route the request to the corresponding handler."""
    response = Response(
        http_version=request.http_version, http_status_code=HttpStatusCode.NOT_FOUND
    )
    # Create a Response object
    if request.path == "/":
        response = Response(
            http_version=request.http_version, http_status_code=HttpStatusCode.OK
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
    elif (
        request.path.startswith("/files/")
        and directory_path
        and request.http_method == HttpMethod.GET
    ):
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
    elif (
        request.path.startswith("/files/")
        and directory_path
        and request.http_method == HttpMethod.POST
    ):
        file_path = request.path.split("/files/")[1]
        with open(f"{directory_path}/{file_path}", "w", encoding="UTF-8") as file:
            file.write(request.body)
        response = Response(
            http_version=request.http_version,
            http_status_code=HttpStatusCode.CREATED,
        )
    return response
