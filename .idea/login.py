from upstox_api.api import *

def login():
    s = Session('your_api_key')
    s.set_redirect_uri('your_redirect_uri')
    s.set_api_secret('your_api_secret')
    print (s.get_login_url())
    s.set_code('your_code_from_login_response')
    access_token = s.retrieve_access_token()
    print ('Received access_token: %s' % access_token)
    u = Upstox('your_api_key', access_token)
    print (u.get_balance())  # get balance / margin limits
    print (u.get_profile())  # get profile
    print (u.get_holdings())  # get holdings
    print (u.get_positions())  # get positions

