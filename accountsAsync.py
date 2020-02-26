import requests
import endpoints
from account import Account
import grequests
import asyncio
import threading
import time


class AccountsAsync:

    def __init__(self, access_token):
        self.access_token = access_token
        self.headers = {"Authorization": "Bearer " + self.access_token}
        self.payload = {}
        self.list_of_accounts = []
        self.complete = False

    '''
    returns list of dicts
    call the accounts endpoint.
    start a new thread to poll the response until a success or failed 
    (i.e. request complete) is received using the result_uri
    '''

    def process_results(self, response):
        response = response.json()
        status = response["status"]

        if status == "Succeeded":
            self.handle_success(response["results"])  # list of dicts
            return
        elif status == "Failed":
            self.handle_failure()

    def handle_success(self, results):
        for account in results:  # list of dicts
            print(account)
            self.list_of_accounts.append(Account(account))
        self.complete = True

    def handle_failure(self):
        print("Failed..................")
        self.complete = True

    def get_accounts(self):
        response = requests.request("GET", endpoints.get_accounts_url + "?async=true&webhook_uri=https://localhost:8000",
                                    headers=self.headers,
                                    data=self.payload,
                                    hook={'response': self.process_results}).json()
        self.complete = False
        while not self.complete:
            time.sleep(1)
            results_uri = response["results_uri"]
            task_id = response["task_id"]
            requests.request("GET", endpoints.get_accounts_url + "?async=true",
                             headers=self.headers,
                             data=self.payload,
                             hook={'response': self.call_results_uri}).json()

        '''get all transactions for all accounts of a client'''
    def get_all_transactions_for_all_accounts(self):
        number_of_accounts = 0
        for account in self.accounts:
            transactions, outcome = self.get_account_transactions(account["account_id"])
            if outcome == "Succeeded":
                self.transactions.append(transactions)
            number_of_accounts += 1
        return self.transactions

    '''get all transactions for a specific account id'''
    def get_account_transactions(self, account_id) -> tuple:
        payload = {}
        headers = {"Authorization": "Bearer " + self.__access_token}
        response = requests.request("GET", endpoints.get_accounts_url + "/" + account_id + "/transactions",
                                    headers=headers, data=payload).json()
        transactions = response["results"]
        outcome = response["status"]
        return transactions, outcome

