import json


class Account:

    def __init__(self, account_details: dict):
        self.__account_details = account_details
        self.account_id = account_details["account_id"]
        self.update_timestamp = account_details["update_timestamp"]
        self.account_type = account_details["account_type"]
        self.display_name = account_details["display_name"]
        self.currency = account_details["currency"]
        self.account_number = account_details["account_number"]["number"]
        self.swift_bic = account_details["account_number"]["swift_bic"]
        self.sort_code = account_details["account_number"]["sort_code"]
        self.provider_name = account_details["provider"]["display_name"]
        self.logo_uri = account_details["provider"]["logo_uri"]
        self.provider_id = account_details["provider"]["provider_id"]
        self.transactions = None

    def __str__(self):
        return json.dumps(self.__account_details, indent=2)
