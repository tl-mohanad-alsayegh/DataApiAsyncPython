base_url = "https://auth.truelayer-sandbox.com"

'''Authentication'''
refresh_token_url = base_url + "/connect/token"
exchange_code_url = base_url + "/connect/token"

'''Accounts'''
api_base_url = "https://api.truelayer-sandbox.com"
accounts_base_url = api_base_url + "/data/v1"
get_accounts_url = accounts_base_url + "/accounts"
get_accounts_url_async = get_accounts_url + "/?async=true"
