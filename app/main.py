import socket

# Constants
CRLF = "\r\n"
END_HEADERS = CRLF + CRLF
RESPONSE_200 = "HTTP/1.1 200 OK" + END_HEADERS
BUFFER_ZISE = 1024


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    # print("Logs from your program will appear here!")

    # Create a TCP socket
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)

    # Accept the connection from TCP client
    while True:
        client_socket, client_address = server_socket.accept()

        with client_socket:
            # Receive the data from client
            data = client_socket.recv(BUFFER_ZISE)
            # Response 200 OK
            client_socket.send(RESPONSE_200.encode())

if __name__ == "__main__":
    main()
