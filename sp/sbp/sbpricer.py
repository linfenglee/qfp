from typing import Tuple
import numpy as np
from scipy.stats import norm

from sp.base import MarketInfo, ModelInfo, ContractInfo


class SBPricer(object):
    """
    MC for SFD500 structure product (Snow Ball)
    """

    def __init__(
            self, market_info: MarketInfo, contract_info: ContractInfo, model_info: ModelInfo
    ):
        """"""
        # market information
        self.sp = market_info.stock_price
        self.r = market_info.interest_rate
        self.q = market_info.dividend
        self.vol = market_info.volatility

        # contract information
        self.c = contract_info.coupon
        self.k = contract_info.strike
        self.start_date = contract_info.start_date
        self.end_date = contract_info.end_date
        # self.continuous_monitor = contract_info.continuous_monitor
        self.monitor_dates = contract_info.monitor_dates
        self.upper = market_info.stock_price * contract_info.up_level
        self.lower = market_info.stock_price * contract_info.down_level

        # model information
        self.paths = model_info.paths
        # self.time_steps = model_info.time_steps
        self.valuation_date = model_info.valuation_date
        self.extra_time = (self.valuation_date - self.start_date).days / 365
        self.time_period = (self.end_date - self.start_date).days / 365
        self.time_maturity = (self.end_date - self.valuation_date).days / 365
        self.time_steps = model_info.time_steps
        self.dt = self.time_maturity / self.time_steps

        self.monitor_steps = self.get_monitor_steps()

    def get_monitor_steps(self):
        """"""
        monitor_steps = []
        for mdt in self.monitor_dates:
            if mdt > self.valuation_date:
                monitor_steps.append(int((mdt - self.valuation_date).days / 365 / self.dt))
        return monitor_steps

    def show_process(self, path: int) -> None:
        """"""
        percent = round(100 * path / self.paths, 3)
        print("#" * int(percent) + f" {percent}%", end="\r")

    def mc_engine(self):
        """"""
        pfs, svs = [], []
        drift = (self.r - self.q - 0.5 * np.square(self.vol)) * self.dt
        diffusion = self.vol * norm.rvs(0, 1, (self.paths, self.time_steps)) * np.sqrt(self.dt)
        st = np.insert(self.sp * np.cumprod(np.exp(drift + diffusion), axis=1), 0, self.sp, axis=1)
        for path in range(self.paths):
            s = st[path, :]
            idx = np.argwhere(s[self.monitor_steps] >= self.upper)
            if len(idx) > 0:
                t = self.monitor_steps[idx[0][0]] * self.dt
                df = np.exp(-self.r * (t + 1 / 365))
                pf = df * (1 + self.c * (t + self.extra_time))
                sv = t + self.extra_time
            else:
                df = np.exp(-self.r * (self.time_maturity + 1 / 365))
                sv = self.time_period
                if np.any(s <= self.lower):
                    pf = df * min(s[-1] / self.sp, self.k)
                else:
                    pf = df * (1 + self.c * self.time_period)
            pfs.append(pf)
            svs.append(sv)

            self.show_process(path)

        return np.array(pfs), np.array(svs)

    def run(self) -> Tuple:
        """"""

        payoffs, survivals = self.mc_engine()

        print("=" * 60)
        print("SFD500")
        print("=" * 60)
        print(
            f"MC value: {round(payoffs.mean(), 5)} | MC standard error: {round(payoffs.std() / np.sqrt(self.paths), 5)}")
        print(
            f"MC survival for SFD500: {round(survivals.mean(), 5)} | MC standard error: {round(survivals.std() / np.sqrt(self.paths), 5)}")

        return payoffs, survivals
