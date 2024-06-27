"""Log module."""

import datetime
from app.server.http import Request, Response


def log_request(client_address, request: Request, response: Response):
    """Print the request in log."""
    date_time = datetime.datetime.now()
    date_time_format = date_time.strftime("%d/%m/%Y %H:%M:%S")
    print(
        f"[{date_time_format}] {response.http_status_code.code} {request.http_method} {request.path} {client_address[0]} - {client_address[1]} - {request.user_agent}"
    )
