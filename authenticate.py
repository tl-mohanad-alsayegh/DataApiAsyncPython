import json
import requests
import endpoints


class Authentication:

    def __init__(self):
        self.client_secrets = {}
        self.read_client_secrets()
        self.write_client_secrets()
        if self.client_secrets["refresh_token"]:
            print("Found refresh token, refreshing exchange code")
            self.__refresh_token()
        else:
            print("No refresh token, exchanging code")
            self.__exchange_code_for_access_token()

    def __refresh_token(self):
        payload = {
            "grant_type": "refresh_token",
            "client_id": self.client_secrets["client_id"],
            "client_secret": self.client_secrets["client_secret"],
            "refresh_token": self.client_secrets["refresh_token"]
        }
        headers = {}

        response = requests.request("POST", endpoints.refresh_token_url, headers=headers, data=payload).json()
        self.update_client_secrets(response["refresh_token"], response["access_token"])
        self.write_client_secrets()
        print(json.dumps(response, indent=2))

    def __exchange_code_for_access_token(self):
        payload = {
            "grant_type": "authorization_code",
            "client_id": self.client_secrets["client_id"],
            "client_secret": self.client_secrets["client_secret"],
            "redirect_uri": self.client_secrets["redirect_uri"],
            "code": self.client_secrets["exchange_code"]
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept': '*/*',
            'Host': 'auth.truelayer-sandbox.com',
        }

        response = requests.request("POST", endpoints.exchange_code_url, headers=headers, data=payload).json()
        self.update_client_secrets(response["refresh_token"], response["access_token"])
        self.write_client_secrets()
        print(json.dumps(response, indent=2))

    def read_client_secrets(self):
        with open("secrets.json", "r") as secrets:
            secrets_json = json.load(secrets)
        self.client_secrets["client_id"] = secrets_json["client_id"]
        self.client_secrets["client_secret"] = secrets_json["client_secret"]
        self.client_secrets["redirect_uri"] = secrets_json["redirect_uri"]
        self.client_secrets["exchange_code"] = secrets_json["exchange_code"]
        self.client_secrets["refresh_token"] = secrets_json["refresh_token"]

    def write_client_secrets(self):
        with open("secrets.json", "w") as secrets:
            json.dump(self.client_secrets, secrets, indent=2)

    def update_client_secrets(self, refresh_token=None, access_token=None):
        self.client_secrets["refresh_token"] = refresh_token
        self.client_secrets["access_token"] = access_token


auth = Authentication()
print("Printing client secrets...")
print(json.dumps(auth.client_secrets, indent=2))