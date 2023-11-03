"""A simple HTTP server."""
import socket
import threading

from app.server.constant import HOST, PORT
from app.server.server import server_handler
from app.server.log import print_welcome_message
from app.server.utils import get_directory_path


def main():
    """The main function."""
    # Get the directory path from the command line arguments
    directory_path = get_directory_path()
    # Create a TCP socket
    server_socket = socket.create_server((HOST, PORT), reuse_port=True)
    server_socket.listen()
    # Print the welcome message
    print_welcome_message()
    # Keep the server running forever
    while True:
        # Accept the connection from TCP client
        client_socket, client_address = server_socket.accept()
        # Create a thread to handle the client connection
        thread = threading.Thread(
            target=server_handler, args=(client_socket, client_address, directory_path)
        )
        thread.start()


if __name__ == "__main__":
    main()
