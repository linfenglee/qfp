from typing import Tuple
from dataclasses import dataclass
from datetime import datetime


@dataclass
class MarketInfo:
    """"""
    interest_rate: float = 0.0225
    stock_price: float = 5.1
    volatility: float = 0.3
    dividend: float = 0.0


@dataclass
class ContractInfo:
    """"""
    coupon: float = 0.31
    strike: float = 1.0
    start_date: datetime = datetime(2019, 1, 4)
    end_date: datetime = datetime(2019, 12, 27)
    monitor_dates: Tuple = (
        datetime(2019, 2, 1), datetime(2019, 3, 4), datetime(2019, 3, 29),
        datetime(2019, 4, 26), datetime(2019, 5, 31), datetime(2019, 6, 28),
        datetime(2019, 7, 26), datetime(2019, 8, 23), datetime(2019, 9, 20),
        datetime(2019, 10, 25), datetime(2019, 11, 22), datetime(2019, 12, 27)
    )
    up_level: float = 1.03
    down_level: float = 0.7


@dataclass
class ModelInfo:
    """"""
    paths: int = 50000
    time_steps: int = 3650
    valuation_date: datetime = datetime(2019, 1, 3)