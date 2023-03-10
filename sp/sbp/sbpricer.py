from typing import Tuple
import numpy as np

from sp.constant import Annual
from sp.base import MarketInfo, ModelInfo, BSContractInfo
from sp.pricer import MCPricer


class SBPricer(MCPricer):
    """
    MC for SFD500 structure product (Snow Ball)
    """

    def __init__(
            self,
            market_info: MarketInfo,
            contract_info: BSContractInfo,
            model_info: ModelInfo
    ):
        """"""
        super().__init__(market_info, model_info)

        # contract information
        self.c = contract_info.coupon
        self.k = contract_info.strike
        self.start_date = contract_info.start_date
        self.end_date = contract_info.end_date
        self.monitor_dates = contract_info.monitor_dates
        self.upper = market_info.stock_price * contract_info.up_level
        self.lower = market_info.stock_price * contract_info.down_level

        self.extra_time = (self.valuation_date - self.start_date).days / Annual
        self.time_period = (self.end_date - self.start_date).days / Annual

        self.monitor_steps = self.get_monitor_steps()

    def get_monitor_steps(self):
        """"""
        monitor_steps = []
        for mdt in self.monitor_dates:
            if mdt > self.valuation_date:
                monitor_steps.append(int((mdt - self.valuation_date).days / Annual / self.dt))
        return monitor_steps

    def mc_engine(self):
        """"""
        pfs, svs = [], []
        st = self.simulate_st()
        for path in range(self.paths):
            s = st[path, :]
            idx = np.argwhere(s[self.monitor_steps] >= self.upper)
            if len(idx) > 0:
                t = self.monitor_steps[idx[0][0]] * self.dt
                df = np.exp(-self.r * (t + 1 / Annual))
                pf = df * (1 + self.c * (t + self.extra_time))
                sv = t + self.extra_time
            else:
                df = np.exp(-self.r * (self.tau + 1 / Annual))
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
