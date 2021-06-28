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
            with open(self.path, "a+") as f:
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
        dict = self.keys
        print(user)
        print(pswd)
        print(dict)

        # check if the password equals the usernames password
        try:
            if pswd == self.keys[user]:
                return True
            elif pswd != self.keys[user]:
                return False
        except:
            # this case is if the user does not exist in the file
            self.keys[user] = pswd
            json.dump(self.keys, self.path)
            return True
