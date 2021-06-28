from brownie import accounts, config, interface, network
from web3 import Web3
from scripts.get_weth import get_weth
from scripts.helpful_scripts import get_account, approve_erc20
from scripts.swap.swap import swap
from scripts.aave.aave_borrow import get_lending_pool, get_borrowable_data, borrow_erc20
from scripts.chainlink.chainlink import get_asset_price

amount = Web3.toWei(0.1, "ether")


def main():
    account = get_account()
    weth_address = config["networks"][network.show_active()]["weth_token"]
    dai_address = config["networks"][network.show_active()]["aave_dai_token"]
    if network.show_active() in ["mainnet-fork"]:
        get_weth(account=account)
    print(
        f"Starting ETH Balance is: {interface.IERC20(weth_address).balanceOf(account.address)}"
    )
    print(
        f"Starting DAI Balance is: {interface.IERC20(dai_address).balanceOf(account.address)}"
    )
    lending_pool = get_lending_pool()
    approve_erc20(amount, lending_pool.address, weth_address, account)
    print("Depositing...")
    lending_pool.deposit(weth_address, amount, account.address, 0, {"from": account})
    print("Deposited!")
    borrowable_eth, total_debt_eth = get_borrowable_data(lending_pool, account)
    print("LETS BORROW IT ALL")
    dai_eth_price = get_asset_price()
    amount_dai_to_borrow = (1 / dai_eth_price) * (borrowable_eth * 0.95)
    print(f"We are going to borrow {amount_dai_to_borrow} DAI")
    borrow_erc20(lending_pool, amount_dai_to_borrow, account, erc20_address=dai_address)
    # Sell the borrowed asset
    # You could use anything like Aave, Uniswap, 1inch, etc
    amount_dai_to_borrow = int(amount_dai_to_borrow * 10 ** 18)
    price_feed = config["networks"][network.show_active()]["dai_eth_price_feed"]
    uniswapv2_router02 = config["networks"][network.show_active()]["uniswapv2_router02"]
    approve_tx = approve_erc20(
        amount_dai_to_borrow, uniswapv2_router02, dai_address, account
    )
    approve_tx.wait(1)
    swap(
        dai_address,
        weth_address,
        amount_dai_to_borrow,
        account,
        price_feed,
        uniswapv2_router02,
    )
    print(
        f"Ending ETH Balance is: {interface.IERC20(weth_address).balanceOf(account.address)}"
    )
    print(
        f"Ending DAI Balance is: {interface.IERC20(dai_address).balanceOf(account.address)}"
    )
    borrowable_eth, total_debt_eth = get_borrowable_data(lending_pool, account)
