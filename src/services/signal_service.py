from data_access.candles_data_access import CandlesDataAccess
from calculator_service import CalculaterService
from helpers.utils import Utils


class SignalService:
    def __init__(self):
        self.candles_data_access = CandlesDataAccess()
        self.calculator_service = CalculaterService()
        self.utils = Utils()

    def extractSignals(self, datas15m, date):
        data15m, candles = self.candles_data_access.get15m(datas15m)
        closeTimes = self.candles_data_access.getCloseTimes(data15m)
        emaValues = self.calculator_service.calculateEmaValues(closeTimes)
        organisedEmaValues = self.utils.arrangementOfEmaValues(emaValues, candles)
        # firstSignal, organisedEmaValues = checkPositionSignal(organisedEmaValues)
        # signals = getSignalsTime(firstSignal, organisedEmaValues, date)
        # return signals
