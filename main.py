# imports
from dydx3 import Client
from web3 import Web3
from pprint import pprint
from datetime import datetime, timedelta

# Use for Testnet
from dydx3.constants import API_HOST_GOERLI

# Use for Mainnet
# from dydx3.constants import API_HOST_MAINNET
# API_HOST_MAINNET


# Constants
ETHEREUM_ADDRESS = "0x701b56343694D762F0AEf29C3d9e7ce678F62D4C"
ETHEREUM_PRIVATE_KEY = "dd8e5f650ab9ae9dd5f90d2a87d671b4e8085d05c173cb02dd8d4a6789f4f630"
STARK_PRIVATE_KEY = "0196ac12f2c2bb145f1f4c941a43f1a11e1896d81e773626dbd807fb6c446cfc"
DYDX_API_KEY = "bd97de70-4c71-7fa5-1dd3-6b679d761c20"
DYDX_API_SECRET = "4VN3FWF6Fe3f7iaY1ursYZsi-ARvri9QDu-7fHgy"
DYDX_API_PASSPHRASE = "ACp_ipH1ZWCdIacNJBE2"
HOST = API_HOST_GOERLI

# HTTP PROVIDER
HTTP_PROVIDER = "https://eth-goerli.g.alchemy.com/v2/9yiG5KNiwPaE_Tv1bxVILgneS3bEthPn"

# Create Client Connection
client = Client(
    host = HOST,
    api_key_credentials ={
    "key": DYDX_API_KEY,
    "secret": DYDX_API_SECRET,
    "passphrase": DYDX_API_PASSPHRASE
    },
    stark_private_key= STARK_PRIVATE_KEY,
    eth_private_key = ETHEREUM_PRIVATE_KEY,
    default_ethereum_address = ETHEREUM_ADDRESS,
    web3 = Web3(Web3.HTTPProvider(HTTP_PROVIDER))
)
account = client.private.get_account()
account_id = account.data["account"]["id"]
quote_balance = account.data["account"]["quoteBalance"]


candles= client.public.get_candles(
market = "BTC-USD",
    resolution='1HOUR',
    limit = 3
)
# pprint(candles.data['candles'])


# Get Position ID
account_response = client.private.get_account()
position_id = account_response.data['account']['positionId']

# Get expiration time
server_time = client.public.get_time()
expiration = datetime.fromisoformat(server_time.data['iso'].replace('Z', '')) + timedelta(seconds=70)

def buy():
    global position_id, expiration
    placed_order = client.private.create_order(
      position_id=position_id, # required for creating the order signature
      market="BTC_USD",
      side='BUY',
      order_type="MARKET",
      post_only=False,
      size='0.001',
      price='100000',
      limit_fee='0.015',
      expiration_epoch_seconds=expiration.timestamp(),
      time_in_force='FOK',
      reduce_only = False,
    )

# Place an Order

# server_time.data