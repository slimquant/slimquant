import multiprocessing
from time import sleep
from datetime import datetime, time
from logging import INFO

from vnpy.event import EventEngine
from vnpy.trader.setting import SETTINGS
from vnpy.trader.engine import MainEngine
from vnpy.gateway.okex import OkexGateway
from vnpy.app.algo_trading import AlgoTradingApp
from vnpy.trader.constant import Offset, Direction



SETTINGS["log.active"] = True
SETTINGS["log.level"] = INFO
SETTINGS["log.console"] = True
from .gateway_config import okex_setting


def run_child():
    """
    Running in the child process.
    """
    SETTINGS["log.file"] = True

    event_engine = EventEngine()
    main_engine = MainEngine(event_engine)
    alg_engine = main_engine.add_app(AlgoTradingApp)

    main_engine.add_gateway(OkexGateway)
    main_engine.connect(okex_setting, "OKEX")



    default_setting = {
        "vt_symbol": "XRP-OKB.OKEX",
        "direction": Direction.LONG.value,
        "volume": 1.0,
        "offset": Offset.OPEN.value,
        "template_name":"BestLimitAlgo"
    }
    alg_engine.init_engine()
    alg_engine.start_algo(default_setting)



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
        trading = True#orignal False

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
        print("shit")


if __name__ == "__main__":
    #run_parent()
    run_child()
