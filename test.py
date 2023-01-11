from datetime import datetime

from sp.base import MarketInfo, ModelInfo, BSContractInfo
from sp.sbp.sbpricer import SBPricer


if __name__ == "__main__":

    market_data = MarketInfo(
        interest_rate=2.5 / 100,
        stock_price=1.0,
        volatility=0.30,
        dividend=0.0
    )

    contract_data = BSContractInfo(
        coupon=0.15, strike=1.0,
        start_date=datetime(2022, 10, 1),
        end_date=datetime(2023, 10, 1),
        monitor_dates=(
            datetime(2022, 11, 1), datetime(2022, 12, 1), datetime(2023, 1, 1),
            datetime(2023, 2, 1), datetime(2023, 3, 1), datetime(2023, 4, 1),
            datetime(2023, 5, 1), datetime(2023, 6, 1), datetime(2023, 7, 1),
            datetime(2023, 8, 1), datetime(2023, 9, 1), datetime(2023, 10, 1)
        ),
        up_level=1.03, down_level=0.7
    )
    model_data = ModelInfo(
        paths=50000, time_steps=3650, valuation_date=datetime(2023, 1, 9), end_date=datetime(2023, 10, 1)
    )

    pricer = SBPricer(market_data, contract_data, model_data)
    pricer.run()