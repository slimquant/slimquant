import multiprocessing
from time import sleep
from datetime import datetime, time
from logging import INFO

from vnpy.event import EventEngine
from vnpy.trader.setting import SETTINGS
from vnpy.trader.engine import MainEngine

from vnpy.gateway.okex import OkexGateway
from vnpy.app.cta_strategy import CtaStrategyApp
from vnpy.app.algo_trading import AlgoTradingApp
from vnpy.app.algo_trading.engine import AlgoEngine
#from vnpy.app.algo_trading.algos import EVENT_CTA_LOG
from vnpy.trader.constant import Offset, Direction
from vnpy.trader.object import TradeData, OrderData, TickData
from vnpy.trader.engine import BaseEngine


SETTINGS["log.active"] = True
SETTINGS["log.level"] = INFO
SETTINGS["log.console"] = True



okex_setting = {
    "API Key": "325d079f-dc52-4825-a2ae-906ba3f22a99",
    "Secret Key": "698658F47261CD6E6A9D091232CE6D7A",
    "Passphrase": "wudasea",
    "会话数": 3,
    "代理地址": "",
    "代理端口": "",
}


def run_child():
    """
    Running in the child process.
    """
    SETTINGS["log.file"] = True

    event_engine = EventEngine()
    main_engine = MainEngine(event_engine)
    main_engine.add_gateway(OkexGateway)
    okex_engine = main_engine.add_app(AlgoTradingApp)
    main_engine.connect(okex_setting, "OKEX")


    sleep(10)

    okex_engine.init_engine()
    okex_engine.start_algo()


    """
    okex_engine.init_all_strategies()
    sleep(60)   # Leave enough time to complete strategy initialization
    main_engine.write_log("OKEX策略全部初始化")
    okex_engine.start_all_strategies()
    main_engine.write_log("OKEX策略全部启动")
    """

    while True:
        sleep(1)


def run_parent():
    """
    Running in the parent process.
    """
    print("启动Iceberg策略守护父进程")

    # Chinese futures market trading period (day/night)
    DAY_START = time(8, 45)
    DAY_END = time(15, 30)

    NIGHT_START = time(20, 45)
    NIGHT_END = time(2, 45)

    child_process = None

    while True:
        current_time = datetime.now().time()
        trading = False

        # Check whether in trading period
        if (
            (current_time >= DAY_START and current_time <= DAY_END)
            or (current_time >= NIGHT_START)
            or (current_time <= NIGHT_END)
        ):
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


if __name__ == "__main__":
    run_parent()
