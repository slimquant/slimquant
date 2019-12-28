import multiprocessing
from time import sleep
from datetime import datetime, time
from logging import INFO,DEBUG

from vnpy.event import EventEngine
from vnpy.trader.setting import SETTINGS
from vnpy.trader.engine import MainEngine
from vnpy.gateway.okex import OkexGateway
from vnpy.gateway.binance import BinanceGateway
from vnpy.app.algo_trading import AlgoTradingApp
from vnpy.trader.constant import Offset, Direction



SETTINGS["log.active"] = True
SETTINGS["log.console"] = True
SETTINGS["log.file"] = True
SETTINGS["log.level"] = DEBUG

from gateway_config import okex_setting,binance_setting


def run_child():
    """
    Running in the child process.
    """


    event_engine = EventEngine()
    main_engine = MainEngine(event_engine)
    alg_engine = main_engine.add_app(AlgoTradingApp)

    main_engine.add_gateway(BinanceGateway)
    main_engine.connect(binance_setting, "BINANCE")



    default_setting = {
        "vt_symbol": "LINKUSDT.BINANCE",
        "direction": Direction.LONG.value,
        "price": 1.3,
        "volume": 70,
        "display_volume": 10,
        "interval": 120,
        "offset": Offset.NONE.value,
        "template_name":"IcebergAlgo"
    }
    alg_engine.init_engine()
    alg_engine.start_algo(default_setting)



def run_parent():
    """
    Running in the parent process.
    """
    print("启动策略守护父进程")
    child_process = None

    while True:
        trading = True
        # Start child process in trading period
        if trading and child_process is None:
            print("启动子进程")
            child_process = multiprocessing.Process(target=run_child)
            child_process.start()
            print("子进程启动成功")

        # 非记录时间则退出子进程
        if not trading and child_process is not None:
            print("关闭子进程")
            child_process.terminate()
            child_process.join()
            child_process = None
            print("子进程关闭成功")

        sleep(5)
        print("shit")


if __name__ == "__main__":
    #run_parent()
    run_child()
