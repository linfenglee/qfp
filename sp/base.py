from typing import Tuple
from dataclasses import dataclass
from datetime import datetime

from sp.constant import Annual


@dataclass
class MarketInfo:
    """"""
    interest_rate: float = 0.0225
    stock_price: float = 5.1
    volatility: float = 0.3
    dividend: float = 0.0


@dataclass
class ModelInfo:
    """"""
    paths: int = 50000
    time_steps: int = 3650
    valuation_date: datetime = datetime(2019, 1, 3)
    end_date: datetime = datetime(2020, 1, 4)

    def __post_init__(self):
        """"""
        self.tau = (self.end_date - self.valuation_date).days / Annual
        self.dt = self.tau / self.time_steps


@dataclass
class ContractInfo:
    """"""
    start_date: datetime = datetime(2019, 1, 4)
    end_date: datetime = datetime(2019, 12, 27)


@dataclass
class BSContractInfo(ContractInfo):
    """"""
    coupon: float = 0.31
    strike: float = 1.0
    monitor_dates: Tuple = (
        datetime(2019, 2, 1), datetime(2019, 3, 4), datetime(2019, 3, 29),
        datetime(2019, 4, 26), datetime(2019, 5, 31), datetime(2019, 6, 28),
        datetime(2019, 7, 26), datetime(2019, 8, 23), datetime(2019, 9, 20),
        datetime(2019, 10, 25), datetime(2019, 11, 22), datetime(2019, 12, 27)
    )
    up_level: float = 1.03
    down_level: float = 0.7


@dataclass
class TGContractInfo(ContractInfo):
    """"""
    coupon: float = 0.08
    start_date = datetime(2019, 1, 4)
    end_date: datetime = datetime(2019, 12, 27)
    monitor_dates: Tuple = (
        datetime(2019, 2, 1), datetime(2019, 3, 4), datetime(2019, 3, 29),
        datetime(2019, 4, 26), datetime(2019, 5, 31), datetime(2019, 6, 28),
        datetime(2019, 7, 26), datetime(2019, 8, 23), datetime(2019, 9, 20),
        datetime(2019, 10, 25), datetime(2019, 11, 22), datetime(2019, 12, 27)
    )
    up_level: float = 1.05
    down_level: float = 0.8


@dataclass
class TXContractInfo(ContractInfo):
    """"""
    coupon: float = 0.1
    down_level: float = 0.7


@dataclass
class ACContractInfo(ContractInfo):
    """"""
    modified: bool = False  # @param
    coupon: float = 0.2026  # @param {type:"number"}
    ko_level: float = 0.93  # @param {type:"number"}
    call_strike: float = 0.9  # @param {type:"number"}
    put_strike: float = 0.9  # @param {type:"number"}
    monitor_info: Tuple = (
        (datetime(2021, 6, 4), 0.5),
        (datetime(2021, 11, 4), 1.0),
        (datetime(2022, 4, 4), 1.5)
    )


@dataclass
class FHContractInfo:
    """"""
    coupon: float = 0.015
    start_date = datetime(2019, 1, 4)
    end_date: datetime = datetime(2020, 1, 4)
    monitor_dates: Tuple = (
        datetime(2019, 2, 4), datetime(2019, 3, 4), datetime(2019, 4, 4),
        datetime(2019, 5, 4), datetime(2019, 6, 4), datetime(2019, 7, 4),
        datetime(2019, 8, 4), datetime(2019, 9, 4), datetime(2019, 10, 4),
        datetime(2019, 11, 4), datetime(2019, 12, 4), datetime(2020, 1, 4)
    )
    up_level: float = 1.03
    down_level: float = 0.7



