from datetime import *


def clock(type, message):
    today = date.today()
    return str(
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
        + type.upper()
        + " -> "
        + " "
        + message.replace("+", " ")
        + "\n",
    )
