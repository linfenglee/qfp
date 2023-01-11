from sp.base import (
    MarketInfo, ModelInfo,
    BSContractInfo,
    TGContractInfo,
    TXContractInfo,
    ACContractInfo,
    FHContractInfo
)
from sp.sbp.sbpricer import SBPricer
from sp.tgp.tgpricer import TGPricer
from sp.txp.txpricer import TXPricer
from sp.acp.acpricer import ACPricer
from sp.fhp.fhpricer import FHPricer

if __name__ == '__main__':

    market_data = MarketInfo()
    # contract_data = TGContractInfo()
    # contract_data = TXContractInfo()
    # contract_data = ACContractInfo(modified=False)
    contract_data = FHContractInfo()
    model_data = ModelInfo()

    # pricer = TGPricer(market_data, contract_data, model_data)
    # pricer = TXPricer(market_data, contract_data, model_data)
    # pricer = ACPricer(market_data, contract_data, model_data)
    pricer = FHPricer(market_data, contract_data, model_data)
    pricer.run()


