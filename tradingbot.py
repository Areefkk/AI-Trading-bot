from lumibot.brokers import Alpaca
from lumibot.backtesting import YahooDataBacktesting
from lumibot.strategies.strategy import Strategy
from lumibot.traders import Trader
from datetime import datetime 
from alpaca_trade_api import REST
from timedelta import Timedelta
from finbert_utils import estimate_sentiment

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
    def initialise(self, symbol:str="SPY", cash_at_risk:float):  ## This initialise method will runs once, when the bot starts up
        self.symbol = symbol
        self.sleeptime = "24hr"  ## Dictates how frequently the bot will trade
        self.last_trade = None   ## This captures our last trade, incase we need to undo our buys/sells
        self.cash_at_risk = cash_at_risk
        self.api = REST(base_url = BASE_URL, key_id=API_KEY, secret_key=API_SECRET)

    def position_sizing(self):
        cash = self.get_cash()
        last_price = self.get_last_price(self.symbol)
        quantity = cash * self.cash_At_risk / last_price
        return cash, last_price, quantity
        
    def get_dates():
        today = self.get_datetime()
        three_days_prior = today - Timedelta(days=3)
        return today.strftime('%Y-%m-%d'),three_days_prior('%Y-%m-%d')
    
    def get_sentiment(self):
        today, three_days_prior = self.get_dates()
        news = self.api.get_news(symbol=self.symbol, 
                                 start=three_days_prior, 
                                 end=today)
        news= [ev.__dict__["raw"]["headline"]for ev in news]
        probability,sentiment = estimate_sentiment(news)
        return probability, sentiment

    def on_trading_iteration(self):  ## This iteration will execute everytime new data is retrieved from the data source
        cash, last_price, quantity = self.position_sizing()

        if cash > last_price: ## We're not just buying when we don't have cash
            if sentiment == "positive" and probability > .999: 
                if self.last_order == "sell":
                    self.sell_all() 
                order = self.create_order(
                    self.symbol,
                    quantity,
                    "buy",
                    type="bracket"
                    take_profit_price= last_price*1.20, 
                    stop_loss_price-last_price*.95 
                    )
                self.submit_order(order)
                self.last_trade = "buy"
            elif sentiment == "negative" and probability > .999: 
                if self.last_order == "buy":
                    self.sell_all() 
                order = self.create_order(
                    self.symbol,
                    quantity,
                    "sell",
                    type="bracket"
                    take_profit_price= last_price*.8, 
                    stop_loss_price-last_price*1.05
                    )
                self.submit_order(order)
                self.last_trade = "sell"
        

start_date = datetime(2023,12,15)    
end_date = datetime(2023,12,30)  
broker = Alpaca(ALPACA_CREDS)
strategy = MLTrader(name='mlstrat', broker=broker,
                    parameters={"symbol":"SPY", 
                                "cash_at_risk":.5}) 
strategy.backtest(
    YahooDataBacktesting,
    start_date,
    end_date,
    parameters={}
)
