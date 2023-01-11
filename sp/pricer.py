import numpy as np
from scipy.stats import norm

from sp.base import MarketInfo, ModelInfo


class MCPricer(object):
    """"""

    def __init__(self, market_info: MarketInfo, model_info: ModelInfo):
        """"""

        # market information
        self.sp = market_info.stock_price
        self.r = market_info.interest_rate
        self.q = market_info.dividend
        self.vol = market_info.volatility

        # model information
        self.paths = model_info.paths
        self.time_steps = model_info.time_steps
        self.valuation_date = model_info.valuation_date

        self.tau = model_info.tau
        self.dt = model_info.dt

    def simulate_st(self) -> np.array:
        """"""
        drift = (self.r - self.q - 0.5 * np.square(self.vol)) * self.dt
        diffusion = self.vol * norm.rvs(0, 1, (self.paths, self.time_steps)) * np.sqrt(self.dt)
        st = np.insert(self.sp * np.cumprod(np.exp(drift + diffusion), axis=1), 0, self.sp, axis=1)
        return st

    def show_process(self, path: int) -> None:
        """"""
        percent = round(100 * path / self.paths, 3)
        print("#" * int(percent) + f" {percent}%", end="\r")

    def mc_engine(self):
        """"""
        raise NotImplementedError

    def run(self):
        """"""
        raise NotImplementedError

