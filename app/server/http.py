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

    def validate_accept_encoding(self, accept_encoding: str):
        """Extract the accept encoding from the data."""
        if accept_encoding not in ACCEPT_ENCODING:
            return ""
        return accept_encoding

    def parse_http_request(self, data: bytes):
        """Parse the data from the client into a Request object."""
        data_list = data.decode().split(CRLF)
        data_request_line = data_list.pop(0)
        method, path, http_version = data_request_line.split()
        data_body = data_list.pop(-1)
        data_dict = {
            "Method": method,
            "Path": path,
            "HTTP-Version": http_version,
            "Body": data_body,
        }
        for header in data_list:
            if header:
                key, value = header.split(":", 1)
                data_dict[key] = value
        return data_dict

    def decode(self, data: bytes):
        """Parse the data from the client into a Request object."""
        data_dict = self.parse_http_request(data)
        self.user_agent = data_dict.get("User-Agent", "")
        self.accept = data_dict.get("Accept", "")
        self.accept_encoding = self.validate_accept_encoding(
            accept_encoding=data_dict.get("Accept-Encoding", "")
        )
        self.body = data_dict.get("Body", "")
        self.http_method = HttpMethod(data_dict.get("Method", ""))
        self.path = data_dict.get("Path", "")
        self.http_version = data_dict.get("HTTP-Version", "")


class Response:
    """A class representing a HTTP response."""

    def __init__(
        self,
        http_version: str = "HTTP/1.1",
        http_status_code: HttpStatusCode = HttpStatusCode.OK,
        content_type="text/plain",
        content_encoding: str = "",
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
