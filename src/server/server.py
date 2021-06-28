import socket
import os
import json
import traceback
from datetime import *

# ADD COLOR ESCAPE CODES
class style:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    END = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    # MAYBE ADD IF WINDOWS NO CODES TODO
    if os.name == "nt":
        HEADER = ""
        OKBLUE = ""
        OKCYAN = ""
        OKGREEN = ""
        WARNING = ""
        FAIL = ""
        END = ""
        BOLD = ""
        UNDERLINE = ""


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
            print(
                style.OKGREEN
                + "SERVER -> Created New Server Data Directory"
                + style.END
            )
    if not os.path.isfile(passwordsFile):
        temp = {"admin": "admin"}
        with open(passwordsFile, "w+") as f:
            f.write(json.dumps(temp))
            f.close()
        if verbose:
            print(style.OKGREEN + "SERVER -> Created New Users File" + style.END)
except Exception as e:
    print(e)


print(style.HEADER + "Listening on port %s ..." % SERVER_PORT + style.END)

# util functions for sever
def auth(password):
    # if current password for user is not what its password is
    with open(passwordsFile, "r") as f:
        pfile = json.load(f)
        f.close()

    if password == pfile[username]:
        return True
    else:
        return False


def clock(operation):
    today = date.today()
    with open(currentUserLog, "a+") as f:
        if operation == "in":
            f.writelines(
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
                    + "IN  -> "
                    + " "
                    + requestData[4]
                    + "\n",
                )
            )
        elif operation == "out":
            f.writelines(
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
                    + "OUT -> "
                    + " "
                    + requestData[4]
                    + "\n",
                )
            )
        f.close()


while True:
    try:
        # Wait for client connections
        client_connection, client_address = server_socket.accept()

        # Get the client request
        request = client_connection.recv(1024).decode()

        # Parse HTTP headers
        headers = request.split("\n")
        # print("HEADERS:", headers)

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
                    if requestData[0] == "in" or requestData[0] == "out":
                        # reassign variables for accessing our current users project logs and dirs
                        currentUserDir = "localServerData/" + username + "/"
                        currentProjectDir = currentUserDir + "/" + requestData[3]
                        currentUserLog = currentProjectDir + "/log.txt"

                    # new user case
                    if not os.path.exists(currentUserDir):
                        os.makedirs(currentUserDir)
                        # if this user doesent exist we need to create their login
                        newUser = {username: password}
                        with open(passwordsFile, "w+") as f:
                            f.write(json.dumps(newUser))
                            f.close()
                        if verbose:
                            print(
                                style.OKGREEN
                                + "SERVER -> Created New User Directory"
                                + style.END
                            )
                            print(
                                style.OKGREEN
                                + "SERVER -> Created New User Login"
                                + style.END
                            )

                    # create logs and dirs for current request if they dont exist
                    if not os.path.exists(currentProjectDir):
                        os.makedirs(currentProjectDir)
                        if verbose:
                            print(
                                style.OKGREEN
                                + "SERVER -> Created New User Project Directory"
                                + style.END
                            )

                    if not os.path.isfile(currentUserLog):
                        with open(currentUserLog, "w+") as f:
                            f.write("")
                            f.close()
                        if verbose:
                            print(
                                style.OKGREEN
                                + "SERVER -> Created New User Log"
                                + style.END
                            )

                    authorized = auth(password)

                    if authorized:
                        try:
                            if requestData[0] == "in" or requestData[0] == "out":
                                clock(requestData[0])

                            elif requestData[0] == "changepwd":
                                # TODO WHAT THE FUCK IS WRONG WITH MY CODE
                                """
                                with open(passwordsFile, "w+") as f:
                                    f = json.load(f.read())
                                    f.pop(username)
                                    f.write(json.dumps({username: password}))
                                    f.close()
                                """

                            # respond that we successfully logged the clock in
                            response = normalpost
                        except Exception as e:
                            print(
                                "welp, this was literally never supposed to be reached"
                            )
                            print(e)
                            traceback.print_exc()
                            response = failpost

                    else:
                        response = forbiddenpost

                except Exception as e:
                    print(e)
                    traceback.print_exc()
                    # something fucked up pretty bad to get here :()
                    response = failpost
            else:
                response = "HTTP/1.0 400 NOT FOUND\n\nInvalid Page Request"
        except Exception as e:
            response = "HTTP/1.0 403 NOT FOUND\n\nInternal Server Error :("
            print(e)
            traceback.print_exc()

        print("RESPONDED:", response)

        # Send HTTP response
        client_connection.sendall(response.encode())
        client_connection.close()
    except Exception as e:
        print(e)

# TODO
# RETURN TIME SPENT OVERVIEW ON PROJECTS OR RETURN THE LOG ITSELF
# ALLOW CHANGING PASSWORDS SERVERSIDE
# server backups are basically a necessity
# more verbose real time logging
# LET USER MANUAL LOG CERTAIN HOURS WITH DESC
# fix spaces encoded as plus symbols when logged
# add typing new password twice to accept the change
# BETTER CHECKS FOR THINGS CLIENT SIDE LIKE PASSWORDS WITH SPACES AND TEDIOUS SHIT
