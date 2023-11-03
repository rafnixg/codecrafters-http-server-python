"""A simple HTTP server."""

from app.server.server import Server
from app.server.utils import get_directory_path


def main():
    """The main function."""
    # Get the directory path from the command line arguments
    directory_path = get_directory_path()
    # Create a server
    server = Server(directory_path=directory_path)
    # Add the endpoints
    # Run the server
    server.run()


if __name__ == "__main__":
    main()
