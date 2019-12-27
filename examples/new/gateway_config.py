import yaml

with open('/home/tao/lab/slimquant/.env.yaml') as f:
    data = yaml.load(f, Loader=yaml.FullLoader)
    binance_setting = {
        "key": data['binance']['key'],
        "secret": data['binance']['secret'],
        "session_number": data['binance']['session_number'],
        "proxy_host": data['binance']['proxy_host'],
        "proxy_port": data['binance']['proxy_port'],
    }

    okex_setting = {
        "API Key": data['okex']['api_key'],
        "Secret Key": data['okex']['secret_key'],
        "Passphrase": data['okex']['passphrase'],
        "会话数": data['okex']['session_num'],
        "代理地址": data['okex']['proxy_ip'],
        "代理端口": data['okex']['proxy_port'],
    }
