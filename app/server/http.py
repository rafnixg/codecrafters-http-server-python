"""This module contains the HTTP-related enums."""

from enum import StrEnum, Enum
from app.server.constant import CRLF, END_HEADERS, ACCEPT_ENCODING


class HttpMethod(StrEnum):
    """An enum representing the HTTP methods."""

    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    OPTIONS = "OPTIONS"
    HEAD = "HEAD"


class HttpStatusCode(Enum):
    """An enum representing the HTTP status codes."""

    OK = (200, "OK")
    CREATED = (201, "Created")
    NOT_FOUND = (404, "Not Found")

    def __init__(self, code: int, message: str) -> None:
        self.code = code
        self.message = message


class Request:
    """A class representing a HTTP request."""

    def __init__(self, data: bytes) -> None:
        self.http_method: HttpMethod
        self.path: str
        self.http_version: str
        self.user_agent: str
        self.accept: str
        self.accept_encoding: str
        self.body: bytes
        self.decode(data)

    def extract_http_method(self, data_list: list):
        """Extract the HTTP method from the data."""
        return data_list[0].split()

    def extract_user_agent(self, data_list: list):
        """Extract the user agent from the data."""
        user_agent = data_list[2]
        if user_agent:
            user_agent = user_agent.split(":")[1].strip()
        return user_agent

    def extract_accept(self, data_list: list):
        """Extract the accept from the data."""
        accept = data_list[3]
        if accept:
            accept = accept.split(":")[1].strip()
        return accept

    def extract_accept_encoding(self, data_list: list):
        """Extract the accept encoding from the data."""
        accept_encoding = data_list[4]
        if accept_encoding:
            accept_encoding = accept_encoding.split(":")[1].strip()
        if accept_encoding not in ACCEPT_ENCODING:
            return ""
        return accept_encoding

    def extract_body(self, data_list):
        """Extract the body from the data."""
        return data_list[-1]

    def decode(self, data: bytes):
        """Parse the data from the client into a Request object."""
        data_list = data.decode().split(CRLF)
        http_method, self.path, self.http_version = self.extract_http_method(data_list)
        self.http_method = HttpMethod(http_method)
        self.user_agent = self.extract_user_agent(data_list)
        self.accept = self.extract_accept(data_list)
        self.accept_encoding = self.extract_accept_encoding(data_list)
        self.body = self.extract_body(data_list)


class Response:
    """A class representing a HTTP response."""

    def __init__(
        self,
        http_version: str = "HTTP/1.1",
        http_status_code: HttpStatusCode = HttpStatusCode.OK,
        content_type="text/plain",
        content_encoding: str = None,
        body: str = None,
    ) -> None:
        self.http_version = http_version
        self.http_status_code = http_status_code
        self.body = body
        self.content_type = content_type
        self.content_encoding = content_encoding
        self.content_length = 0 if self.body is None else len(self.body)

    def encode(self) -> bytes:
        """Encode the response into bytes."""
        message = f"{self.http_version} {self.http_status_code.code} {self.http_status_code.message}{CRLF}"
        if self.content_encoding:
            message += f"Content-Encoding: {self.content_encoding}{CRLF}"
        message += f"Content-Type: {self.content_type}{CRLF}"
        message += f"Content-Length: {self.content_length}{END_HEADERS}"
        message += f"{self.body}"
        return message.encode()
