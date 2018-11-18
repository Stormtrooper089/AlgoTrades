import JindalStel as JStel
import Login

#The login to be implemented for the Upstox apito coonect to the market
# cureently contains the backtesting on local data
if __name__ == '__main__':
    loginObject = Login("key", "uri", "value")
    loginObject.__login__()
    JStel.jindalStel()

