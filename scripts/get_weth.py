from brownie import accounts, config, network, interface
from scripts.helpful_scripts import get_account


def main():
    """
    Runs the get_weth function to get WETH
    """
    get_weth()


def get_weth(account=None):
    """
    Mints WETH by depositing ETH.
    """
    account = (
        account if account else get_account()
    )  # add your keystore ID as an argument to this call
    weth = interface.IWeth(config["networks"][network.show_active()]["weth_token"])
    tx = weth.deposit({"from": account, "value": 1000000000000000000})
    print("Received 1 WETH")
    return tx
