from upstox_api.api import *

class loginInit(Session):
    u = None

    def __init__(self, api_key, api_secret, redirect_api, ):
        self.api_key = api_key
        self.api_secret = api_secret
        self.redirect_uri = redirect_api


    def __login__(self):
        s = Session(self.api_key)
        s.set_redirect_uri(self.redirect_api)
        s.set_api_secret(self.api_secret)
        print (s.get_login_url())
        s.set_code('your_code_from_login_response')
        access_token = s.retrieve_access_token()
        print ('Received access_token: %s' % access_token)
        u = Upstox(self.api_key, access_token)
        print (u.get_balance())  # get balance / margin limits
        print (u.get_profile())  # get profile
        print (u.get_holdings())  # get holdings
        print (u.get_positions())  # get positions
