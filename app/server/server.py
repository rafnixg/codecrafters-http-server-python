"""Server package."""
from app.server.constant import BUFFER_ZISE
from app.server.http import Request
from app.server.log import log_request
from app.server.router import router

def server_handler(client_socket, client_address, directory_path):
    """Handle the client connection."""
    # Receive the data from client
    data = client_socket.recv(BUFFER_ZISE)
    # Parse the data into a Request object
    request = Request()
    request.decode(data)
    # Create a Response object
    response = router(directory_path, request)
    # Send the response to client
    client_socket.sendall(response.encode())
    # Print in log for web server
    log_request(client_address, request, response)
    # Close the connection
    client_socket.close()
