from lumibot.brokers import Alpaca
from lumibot.backtesting import YahooDataBacktesting
from lumibot.strategies.strategy import Strategy
from lumibot.traders import Trader
from datetime import datetime 

# Generated via Alpaca
API_KEY = "PKNBRV0GEQP7Q5OQXBUQ" 
API_SECRET = "TBz6Mjl7hNrZ59b7x2N55Qljqr6THKE12gf09uEu"
BASE_URL = "https://paper-api.alpaca.markets"

ALPACA_CREDS = {
    "API_KEY" : API_KEY,
    "API_SECRET" : API_KEY,
    "PAPER" : True
}

class MLTrader(Strategy):
    def initialise(self, symbol:str="SPY"):  ## This initialise method will runs once, when the bot starts up
        self.symbol = symbol
        self.sleeptime = "24hr"  ## Dictates how frequently the bot will trade
        self.last_trade = None   ## This captures our last trade, incase we need to undo our buys/sells
        
    def on_trading_iteration(self):  ## This iteration will execute everytime new data is retrieved from the data source
        if self.last_trade == None:
            order = self.create_order(
                self.symbol,
                10,
                "buy",
                type="market"
            )
            self.submit_order(order)
            self.last_trade = "buy"
        # return super().on_trading_iteration()

start_date = datetime(2023,12,15)    
end_date = datetime(2023,12,30)  
broker = Alpaca(ALPACA_CREDS)
strategy = MLTrader(name='mlstrat', broker=broker,
                    parameters={"symbol":"SPY"}) 
strategy.backtest(
    YahooDataBacktesting,
    start_date,
    end_date,
    parameters={}
)

