import requests as req
import json
import os
import time

dataJsonPath = "src//client//userdata.json"


def clear():
    os.system("cls" if os.name == "nt" else "clear")


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


def header():
    clear()
    print(style.HEADER + "ClockIn Client 2021.6.24 Ryan Zmuda" + style.END)
    try:
        print(style.OKCYAN + "connected to server: " + serverIP + style.END)
    except:
        print(style.FAIL + "not connected to any server" + style.END)
    print()


def configure():
    header()
    print(
        style.FAIL
        + "User data not detected, follow the prompts below to generate it"
        + style.END
    )
    userdata = {
        "username": input("Enter a username: "),
        "password": input("Enter a password: "),
        "ip": input("Enter the IP and port of the server you want to use: "),
    }
    userdata = json.dumps(userdata)
    datajson = open(dataJsonPath, "w")
    datajson.write(userdata)
    datajson.close()
    userdata = json.load(open(dataJsonPath))
    username = userdata["username"]
    password = userdata["password"]
    serverIP = userdata["ip"]


try:
    header()

    if os.path.isfile(dataJsonPath):
        userdata = json.load(open(dataJsonPath))
        username = userdata["username"]
        password = userdata["password"]
        serverIP = userdata["ip"]
    else:
        configure()

except Exception as e:
    print("Critical failure.")
    print(e)

while True:
    header()
    print(style.OKGREEN + "Commands:")
    print('- in <project name> "description of what you plan to do"')
    print('- out <project name> "description of what you\'ve done"')
    print("- reconfigure")
    print(style.END)
    command = input(">")
    clear()
    commands = command.split(" ")
    if commands[0] == "reconfigure":
        configure()
    elif commands[0] == "in":
        try:
            adress = "http://" + serverIP + "/clientupdate"
            data = {
                "operation": "in",
                "username": username,
                "password": password,
                "name": commands[1],
                "description": commands[2],
            }
            serverReturn = req.post(adress, data=data)
            print(serverReturn)
            time.sleep(3)

        except Exception as e:
            print(style.FAIL + 'Command "in" requires 2 arguments.' + style.END)
            print(e)
            time.sleep(3)
