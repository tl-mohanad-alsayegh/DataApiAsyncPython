import json


class Transaction:
    def __init(self, transaction_details: dict):
        self.__transaction_details = transaction_details
        self.timestamp = transaction_details["timestamp"]
        self.description = transaction_details["description"]
        self.transaction_type = transaction_details["transaction_type"]
        self.amount = transaction_details["amount"]
        self.balance = transaction_details["running_balance"]["amount"]

    def __str__(self):
        return json.dumps(self.__transaction_details, indent=2)
