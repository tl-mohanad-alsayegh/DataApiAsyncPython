from flask import Flask, request, jsonify
from account import Account
from transaction import Transaction
from authenticate import *
from pyngrok import ngrok

app = Flask(__name__)
__client_secrets = {}
__accounts_list = []
__transactions_list = []
__webhook_url = None


@app.route("/accounts", methods=["GET", "POST"])
def handle_accounts():
    print("Received response from /accounts")
    print(request)
    response = request.get_json()
    if response["status"] == "Succeeded":
        get_accounts_results(response["results_uri"])  # populates _accounts_list
        for account in __accounts_list:
            get_transactions(account.account_id)  # registers /transactions endpoint as web-hook callback
        return __accounts_list
    else:
        return "Failed with error: " + response["error"]


@app.route("/transactions", methods=["GET", "POST"])
def handle_transactions():
    response = request.json()
    if response["status"] == "Succeeded":
        get_transactions_results(response["results_uri"]) # populates _transactions_list
        return __transactions_list
    else:
        return "Failed with error: " + response["error"]


@app.route("/")
def handle_test():
    return "Async API, <br \>" \
           "<b>Available endpoints:</b> <br \>" \
           "&nbsp <a href=" + __webhook_url + '/authenticate'">/authenticate  </a><br \>" \
                                              "<b>Webhook URIs available:</b> <br \>" \
                                              "&nbsp /accounts <br \>" \
                                              "&nbsp /transactions <br \><br \>" \
                                              "&nbsp After calling /authenticate, the accounts endpoint will be automatically called.<br \>" \
                                              "&nbsp the ngrok server url is passed as a webhook to TrueLayer async api which would call <br \>" \
                                              "&nbsp back when the accounts are processed & ready to view. <br \>"


@app.route("/authenticate")
def handle_authenticate():
    auth = Authentication()
    print("Printing client secrets...")
    print(json.dumps(auth.client_secrets, indent=2))

    call_accounts_endpoint()

    return jsonify(auth.client_secrets)


def read_client_secrets():
    with open("secrets.json", "r") as secrets:
        secrets_json = json.load(secrets)
        __client_secrets["client_id"] = secrets_json["client_id"]
        __client_secrets["client_secret"] = secrets_json["client_secret"]
        __client_secrets["redirect_uri"] = secrets_json["redirect_uri"]
        __client_secrets["exchange_code"] = secrets_json["exchange_code"]
        __client_secrets["refresh_token"] = secrets_json["refresh_token"]
        __client_secrets["access_token"] = secrets_json["access_token"]


def get_accounts_results(results_uri):
    payload = {}
    headers = {"Authorization": "Bearer " + __client_secrets["access_token"]}
    response = requests.request("GET", results_uri, headers=headers, data=payload).json()  # is this correct? does the
    # result give the actual accounts list or a url to where the results are stored? check using postman

    for account_details in response["results"]:
        account = Account(account_details)
        print(account_details)
        __accounts_list.append(account_details)


# registers /transactions endpoint as web-hook callback
def get_transactions(account_id):
    payload = {}
    headers = {"Authorization": "Bearer " + __client_secrets["access_token"]}
    params = {
        "async": True,
        "webhook_uri": __webhook_url + "/transactions"
    }
    response = requests.request("GET",
                                endpoints.get_accounts_url + "/" + account_id,
                                headers=headers, data=payload, params=params).json()
    transactions = response["results"]
    outcome = response["status"]
    return transactions


def get_transactions_results(results_uri):
    payload = {}
    headers = {"Authorization": "Bearer " + __client_secrets["access_token"]}
    response = requests.request("GET", results_uri, headers=headers, data=payload).json()

    for transaction_details in response["results"]:
        transaction = Transaction(transaction_details)
        print(transaction_details)
        __transactions_list.append(transaction_details)


def call_accounts_endpoint():
    payload = {}
    headers = {"Authorization": "Bearer " + __client_secrets["access_token"]}
    print("Sending to:", endpoints.get_accounts_url_async + "&webhook_uri=" + __webhook_url + "/accounts")
    params = {
        "async": True,
        "webhook_uri": __webhook_url + "/accounts"
    }
    response = requests.request("GET", endpoints.get_accounts_url,
                                headers=headers, data=payload, params=params).json()


if __name__ == '__main__':
    public_url = ngrok.connect(proto="http", port=5000)
    print("Ngrok Connected to: ", public_url)
    __webhook_url = public_url
    read_client_secrets()
    app.run()
