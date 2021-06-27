import socket
import os
import json

from datetime import *

# verbose setting
verbose = True

# define server post defualts
normalpost = "HTTP/1.0 200 OK\n\n"
failpost = "HTTP/1.0 500 OH FUCK...\n\n"
forbiddenpost = "HTTP/1.0 403 Forbidden. Password for user is incorrect.\n\n"

# Define socket host and port
SERVER_HOST = "192.168.56.1"
SERVER_PORT = 7676

# Create socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(1)
try:
    # set server dirs and do other initialization shit
    passwordsDir = "localServerData/"
    passwordsFile = passwordsDir + "logins.json"
    if not os.path.exists(passwordsDir):
        os.makedirs(passwordsDir)
        if verbose:
            print("SERVER -> Created New Server Data Directory")
    if not os.path.isfile(passwordsFile):
        temp = {"admin": "admin"}
        with open(passwordsFile, "w+") as f:
            f.write(json.dumps(temp))
            f.close()
        if verbose:
            print("SERVER -> Created New Users File")
except Exception as e:
    print(e)


print("Listening on port %s ..." % SERVER_PORT)

while True:
    try:
        # Wait for client connections
        client_connection, client_address = server_socket.accept()

        # Get the client request
        request = client_connection.recv(1024).decode()

        # Parse HTTP headers
        headers = request.split("\n")
        print("HEADERS:", headers)

        filename = headers[0].split()[1]

        data = headers[9].split("&")
        requestData = []
        for node in data:
            requestData.append(node.split("=")[1])
        if verbose:
            print(requestData)

        try:
            if filename == "/clientupdate":
                try:
                    # temp new vars using data
                    username = requestData[1]
                    password = requestData[2]

                    # reassign variables for accessing our current users project logs and dirs
                    currentUserDir = "localServerData/" + username + "/"
                    currentProjectDir = currentUserDir + "/" + requestData[3]
                    currentUserLog = currentProjectDir + "/log.txt"

                    # create logs and dirs for current request if they dont exist

                    if not os.path.exists(currentProjectDir):
                        os.makedirs(currentProjectDir)
                        if verbose:
                            print("SERVER -> Created New User Project Directory")

                        # if this user doesent exist we need to create their login
                        newUser = {username: password}
                        with open(passwordsFile, "w+") as f:
                            f.write(json.dumps(newUser))
                            f.close()

                    if not os.path.isfile(currentUserLog):
                        with open(currentUserLog, "w+") as f:
                            f.write("")
                            f.close()
                        if verbose:
                            print("SERVER -> Created New User Log")

                    with open(passwordsFile, "r") as f:
                        passwordsFile = json.loads(passwordsFile)
                        # if current password for user is not what its password is
                        if password != passwordsFile[username]:
                            client_connection.sendall(forbiddenpost.encode())
                            client_connection.close()
                        f.close()

                    if requestData[0] == "in":
                        today = date.today()
                        with open(currentUserLog, "w+") as f:
                            f.write(
                                str(
                                    "["
                                    + " "
                                    + str(today.month)
                                    + "."
                                    + str(today.day)
                                    + "."
                                    + str(today.year)
                                    + " "
                                    + str(datetime.now().hour)
                                    + ":"
                                    + str(datetime.now().minute)
                                    + " "
                                    + "]"
                                    + " "
                                    + "CLOCK IN -> "
                                    + " "
                                    + requestData[4],
                                )
                            )
                            f.close()

                    # respond that we successfully logged the clock in
                    response = normalpost
                except Exception as e:
                    print(e)
                    # something fucked up pretty bad to get here :()
                    response = failpost
            else:
                response = "HTTP/1.0 400 NOT FOUND\n\nInvalid Page Request"
        except Exception as e:
            response = "HTTP/1.0 403 NOT FOUND\n\nInternal Server Error :("
            print(e)

        print("RESPONDED:", response)

        # Send HTTP response
        client_connection.sendall(response.encode())
        client_connection.close()
    except Exception as e:
        print(e)

# TODO
# PASSWORDS
# RETURN TIME SPENT OVERVIEW ON PROJECTS OR RETURN THE LOG ITSELF
# IMPLEMENT OTHER COMMANDS
# ALLOW CHANGING PASSWORDS SERVERSIDE
# server backups are basically a necessity
