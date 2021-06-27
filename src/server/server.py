import socket

# define server post defualts
normalpost = "HTTP/1.0 200 OK\n\n"

# Define socket host and port
SERVER_HOST = "192.168.56.1"
SERVER_PORT = 7676

# Create socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(1)
print("Listening on port %s ..." % SERVER_PORT)

while True:
    # Wait for client connections
    client_connection, client_address = server_socket.accept()

    # Get the client request
    request = client_connection.recv(1024).decode()

    # Parse HTTP headers
    headers = request.split("\n")
    print("HEADERS:", headers)

    filename = headers[0].split()[1]

    try:
        if filename == "/clientupdate":
            response = normalpost

        else:
            response = "HTTP/1.0 400 NOT FOUND\n\nInvalid Page Request"
    except Exception as e:
        response = "HTTP/1.0 403 NOT FOUND\n\nServer Error :("
        print(e)

    print("RESPONDED:", response)

    # Send HTTP response
    client_connection.sendall(response.encode())
    client_connection.close()