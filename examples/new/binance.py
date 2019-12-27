#%%
from vnpy.app.script_trader import init_cli_trading
from vnpy.gateway.binance import BinanceGateway
import yaml
from .gateway_config import binance_setting
engine = init_cli_trading([BinanceGateway])
engine.connect_gateway(binance_setting, "BINANCE")



#%%

engine.get_all_contracts(use_df=True)

#

# 查询所有合约
#print(engine.get_all_contracts(use_df=True).to_string())

# 查询资金
#print(engine.get_all_accounts(use_df=True).to_string())

# 查询持仓
#print(engine.get_tick(vt_symbol="XRP-OKB.OKEX", use_df=True).to_string())



#%%

#engine.start_strategy("/home/tao/lab/slimquant/examples/new/script_demo.py")

