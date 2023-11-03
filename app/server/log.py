"""Log module."""
import datetime
from app.server.http import Request, Response
from app.server.constant import HOST, PORT

def log_request(client_address, request: Request, response: Response):
    """Print the request in log."""
    date_time = datetime.datetime.now()
    date_time_format = date_time.strftime("%d/%m/%Y %H:%M:%S")
    print(
        f"[{date_time_format}] {response.http_status_code.code} {request.http_method} {request.path} {client_address[0]} - {client_address[1]} - {request.user_agent}"
    )

def print_welcome_message():
    """Print the welcome message."""
    print(f"Listening on {HOST}:{PORT}...")
    print("Press Ctrl+C to quit.\n")
    print("Available endpoints:")
    print("GET /")
    print("GET /echo/<message>")
    print("GET /user-agent")
    print("GET /files/<filename>")
    print("POST /files/<filename>")
