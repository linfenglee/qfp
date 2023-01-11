from typing import Tuple
import numpy as np

from sp.constant import Annual
from sp.base import MarketInfo, ModelInfo, ACContractInfo
from sp.pricer import MCPricer


class ACPricer(MCPricer):
    """
    MC for AutoCall structure product
    """

    def __init__(
            self,
            market_info: MarketInfo,
            contract_info: ACContractInfo,
            model_info: ModelInfo
    ):
        """"""
        super().__init__(market_info, model_info)

        # contract information
        self.modified = contract_info.modified
        self.c = contract_info.coupon
        self.ko = contract_info.ko_level
        self.ck = contract_info.call_strike
        self.pk = contract_info.put_strike
        self.sd = contract_info.start_date
        self.ed = contract_info.end_date
        self.mif = contract_info.monitor_info

        self.extra_time = (self.valuation_date - self.sd).days / Annual
        self.time_period = (self.ed - self.sd).days / Annual

        self.monitor_info = self.get_monitor_steps()

    def get_monitor_steps(self):
        """"""
        monitor_info = []
        for mdt, mmp in self.mif:
            if mdt > self.valuation_date:
                monitor_info.append((int((mdt - self.valuation_date).days / Annual / self.dt), mmp))
        return dict(monitor_info)

    def mc_engine(self) -> Tuple:
        """
        mc pricing engine
        """

        pfs, svs = [], []
        st = self.simulate_st()
        monitor_steps = list(self.monitor_info.keys())
        for path in range(self.paths):
            s = st[path, :]
            s0 = s[0]
            idx = np.argwhere(s[monitor_steps] / s0 >= self.ko)
            if len(idx) > 0:
                t = monitor_steps[idx[0][0]] * self.dt
                df = np.exp(-self.r * (t + 1 / Annual))
                pf = df * (1 + self.c * self.monitor_info[monitor_steps[idx[0][0]]])
                sv = t + self.extra_time
            else:
                df = np.exp(-self.r * (self.tau + 1 / Annual))
                sv = self.time_period
                if self.modified:
                    pf = df * (1 - 1 / self.pk * max(self.pk - s[-1] / s0, 0) + 1.5 * self.c / (self.ko - self.ck) * max(s[-1] / s0 - self.ck, 0))
                else:
                    pf = df * (1 - 1 / self.pk * max(self.pk - s[-1] / s0, 0))

            pfs.append(pf)
            svs.append(sv)

            self.show_process(path)

        return np.array(pfs), np.array(svs)

    def run(self) -> Tuple:
        """"""

        pfs, svs = self.mc_engine()

        print("=" * 60)
        print("Auto Call")
        print("=" * 60)
        print(
            f"MC value: {round(pfs.mean(), 5)} | MC standard error: {round(pfs.std() / np.sqrt(self.paths), 5)}")
        print(
            f"MC survival for SFD500: {round(svs.mean(), 5)} | MC standard error: {round(svs.std() / np.sqrt(self.paths), 5)}")

        return pfs, svs
