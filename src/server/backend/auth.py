import json
import os


class authenticator:
    def __init__(self, path):
        # normal self variables
        self.path = path

        # validate filesystem if not exists
        root = path.split("/")[0]
        if not os.path.exists(root):
            os.makedirs(root)

        # create passwords file if not exists
        if not os.path.isfile(path):
            with open(self.path, "w+") as f:
                json.dump({"admin": "admin"}, f)
                f.close()

        # get our initial dict of keys
        authenticator.refresh(self)

    def refresh(self):
        # Opens the specified path to keys by the server as a dict variable
        with open(self.path, "r") as f:
            self.keys = json.load(f)
            f.close()

    def checkAccess(self, user, pswd):
        # refresh our keys incase we have written since
        authenticator.refresh(self)
        # create new login if not exists
        if not user in self.keys:
            self.keys[user] = pswd

            with open(self.path, "w+") as f:
                json.dump(self.keys, f)
                f.close()

        # check if the password equals the usernames password
        if pswd == self.keys[user]:
            return True
        elif pswd != self.keys[user]:
            return False

    def changePassword(self, user, pswd, newpass):
        # refresh our keys incase we have written since
        authenticator.refresh(self)
        if authenticator.checkAccess(self, user, pswd):
            self.keys[user] = newpass
            with open(self.path, "w+") as f:
                json.dump(self.keys, f)
                f.close()
