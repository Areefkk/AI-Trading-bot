# AI-Trading-bot
The main focus of this project is to create an AI powered trading bot which is completely automated. The trader bot will look at sentiment of live news events and trade appropriately according to this.

## Alpaca-trade-api-python

In order to create this trading bot we use alpaca-trade-api-python, which` is a python library for the [Alpaca Commission Free Trading API](https://alpaca.markets).
It allows rapid trading algo development easily, with support for
both REST and streaming data interfaces. 
### API Keys
To use this package you first need to obtain an API key. Go here to [signup](https://app.alpaca.markets/signup)

# Setup
1. Create a virtual environment `conda create -n trader python=3.10` 
2. Activate it `conda activate trader`
3. Install initial deps `pip install lumibot timedelta alpaca-trade-api==3.1.1`
4. Install transformers and friends `pip install torch torchvision torchaudio transformers` 
5. Update the `API_KEY` and `API_SECRET` with values from your Alpaca account 
6. Run the bot `python tradingbot.py`
