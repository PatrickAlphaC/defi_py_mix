from brownie import config, network

price_feed_mapping = {
    "mainnet-fork": {
        (
            config["networks"][network.show_active()]["aave_dai_token"],
            config["networks"][network.show_active()]["weth_token"],
        ): "0x773616E4D11A78F511299002DA57A0A94577F1F4"
    }
}
#  0.000519450000000000
