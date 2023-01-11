import numpy as np

from sp.constant import Annual
from sp.base import MarketInfo, ModelInfo, TXContractInfo
from sp.pricer import MCPricer


class TXPricer(MCPricer):
    """"""

    def __init__(
          self,
          market_info: MarketInfo,
          contract_info: TXContractInfo,
          model_info: ModelInfo
    ):
        """"""

        super().__init__(market_info, model_info)

        # contract information
        self.c = contract_info.coupon
        self.start_date = contract_info.start_date
        self.end_date = contract_info.end_date
        self.lower = market_info.stock_price * contract_info.down_level

        self.extra_time = (self.valuation_date - self.start_date).days / 365
        self.time_period = (self.end_date - self.start_date).days / 365

    def mc_engine(self) -> np.array:
        """"""
        st = self.simulate_st()
        is_triggered = np.any(st <= self.lower, axis=1)
        df = np.exp(-self.r * (self.time_period + 1 / Annual))
        pfs = 1 + self.c * (1 - is_triggered) + is_triggered * np.minimum(st[:, -1] / self.sp - 1, self.c)
        return np.array(df * pfs)

    def run(self) -> np.array:
        """"""

        pfs = self.mc_engine()

        print("=" * 60)
        print("Tong Xin Option")
        print("=" * 60)
        print(f"MC value: {round(pfs.mean(), 5)} | MC standard error: {round(pfs.std() / np.sqrt(self.paths), 5)}")

        return pfs
