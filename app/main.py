"""A simple HTTP server."""

from app.server.server import Server
from app.server.utils import get_directory_path
from app.server.http import HttpMethod
from app.server.router import (
    index_handler,
    echo_handler,
    user_agent_handler,
    upload_files_handler,
    read_files_handler,
)


def main():
    """The main function."""
    # Get the directory path from the command line arguments
    directory_path = get_directory_path()
    # Create a server
    server = Server(directory_path=directory_path)
    # Add the endpoints
    server.add_route(HttpMethod.GET, "/", index_handler)
    server.add_route(HttpMethod.GET, "/echo/*", echo_handler)
    server.add_route(HttpMethod.GET, "/user-agent", user_agent_handler)
    server.add_route(HttpMethod.GET, "/files/*", read_files_handler)
    server.add_route(HttpMethod.POST, "/files/*", upload_files_handler)
    # Run the server
    server.run()


if __name__ == "__main__":
    main()
