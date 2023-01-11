from typing import Tuple
import numpy as np

from sp.constant import Annual
from sp.base import MarketInfo, ModelInfo, FHContractInfo
from sp.pricer import MCPricer


class FHPricer(MCPricer):
    """"""

    def __init__(
            self,
            market_info: MarketInfo,
            contract_info: FHContractInfo,
            model_info: ModelInfo
    ):
        """"""
        super().__init__(market_info, model_info)

        # contract information
        self.c = contract_info.coupon
        self.start_date = contract_info.start_date
        self.end_date = contract_info.end_date
        # self.continuous_monitor = contract_info.continuous_monitor
        self.monitor_dates = contract_info.monitor_dates
        self.upper = market_info.stock_price * contract_info.up_level
        self.lower = market_info.stock_price * contract_info.down_level

        self.extra_time = (self.valuation_date - self.start_date).days / 365
        self.time_period = (self.end_date - self.start_date).days / 365

        self.monitor_steps = self.get_monitor_steps()

    def get_monitor_steps(self):
        """"""
        monitor_steps = []
        for mdt in self.monitor_dates:
            if mdt > self.valuation_date:
                monitor_steps.append(int((mdt - self.valuation_date).days / Annual / self.dt))
        return monitor_steps

    def mc_engine(self) -> Tuple:
        """
        mc pricing engine
        """

        pfs, svs = [], []
        st = self.simulate_st()
        for path in range(self.paths):
            s = st[path, :]
            idx = np.argwhere(s[self.monitor_steps] >= self.upper)
            if len(idx) > 0:
                count = len(np.argwhere(s[self.monitor_steps[:idx[0][0]]] >= self.lower))
                t = self.monitor_steps[idx[0][0]] * self.dt
                df = np.exp(-self.r * (t + 1 / Annual))
                pf = df * (1 + self.c * count)
                sv = t + self.extra_time
            else:
                count = len(np.argwhere(s[self.monitor_steps] >= self.lower))
                df = np.exp(-self.r * (self.tau + 1 / Annual))
                sv = self.time_period
                if np.any(s <= self.lower):
                    pf = df * (1 + self.c * count + min(s[-1] / self.sp - 1, 0))
                else:
                    pf = df * (1 + self.c * count)
            pfs.append(pf)
            svs.append(sv)

            self.show_process(path)

        return np.array(pfs), np.array(svs)

    def run(self) -> Tuple:
        """"""

        pfs, svs = self.mc_engine()

        print("=" * 60)
        print("Pheonix Option")
        print("=" * 60)
        print(
            f"MC value: {round(pfs.mean(), 5)} | MC standard error: {round(pfs.std() / np.sqrt(self.paths), 5)}")
        print(
            f"MC survival: {round(svs.mean(), 5)} | MC standard error: {round(svs.std() / np.sqrt(self.paths), 5)}")

        return pfs, svs
