from vnpy.app.script_trader import init_cli_trading
from vnpy.gateway.okex import OkexGateway
import yaml
with open('/home/tao/lab/slimquant/.env.yaml') as f:
    data = yaml.load(f, Loader=yaml.FullLoader)
    okex_setting = {
        "API Key": data['okex']['api_key'],
        "Secret Key": data['okex']['secret_key'],
        "Passphrase": data['okex']['passphrase'],
        "会话数": data['okex']['session_num'],
        "代理地址": data['okex']['proxy_ip'],
        "代理端口": data['okex']['proxy_port'],
    }

engine = init_cli_trading([OkexGateway])
engine.connect_gateway(okex_setting, "OKEX")

# 查询所有合约
print(engine.get_all_contracts(use_df=True).to_string())

# 查询资金
print(engine.get_all_accounts(use_df=True).to_string())

# 查询持仓
print(engine.get_all_positions(use_df=True).to_string())