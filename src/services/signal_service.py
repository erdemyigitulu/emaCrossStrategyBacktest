
from services.data_processor import DataProcessor

class SignalService:
    def __init__(self):
        self.data_processor = DataProcessor()

    def __getSignalsTime (self , firstSignalSide , emaValues) :
        signalDatas = []
        signalDatas.append(firstSignalSide)
        try :
            for index, value in enumerate(emaValues):
                ema5First = value["ema5"]
                ema8First = value["ema8"]
                ema13First = value["ema13"]
                ema5Next = emaValues[index + 1]["ema5"]
                ema8Next = emaValues[index + 1]["ema8"]
                ema13Next = emaValues[index + 1]["ema13"]
                if (ema8First < ema5First < ema13First) or (ema13First < ema5First < ema8First):
                    if ema5Next > ema8Next and ema5Next > ema13Next:
                        if signalDatas[-1][0] != "long":
                            lst = ["long", emaValues[index + 1]["timestamp"]]
                            signalDatas.append(lst)
                    elif ema5Next < ema8Next and ema5Next < ema13Next:
                        if signalDatas[-1][0] != "short":
                            lst = ["short", emaValues[index + 1]["timestamp"]]
                            signalDatas.append(lst)
                elif ema5First > ema8First > ema13First:
                    if ema5Next < ema8Next and ema5Next < ema13Next:
                        if signalDatas[-1][0] != "short":
                            lst = ["short", emaValues[index + 1]["timestamp"]]
                            signalDatas.append(lst)
                elif ema5First < ema8First < ema13First:
                    if ema5Next > ema8Next and ema5Next > ema13Next :
                        if signalDatas[-1][0] != "long":
                            lst = ["long", emaValues[index + 1]["timestamp"]]
                            signalDatas.append(lst)
        except :
            pass

        return signalDatas

    def extractSignals(self, month , year):
        _ , candleDatas , closeTimeDatas = self.data_processor.getData(month , year)
        organisedEmaValues  = self.data_processor.datasOfEmaValues(closeTimeDatas, candleDatas)
        firstSignalSide = self.data_processor.checkFirstSignalOfPosition(organisedEmaValues)
        signals = self.__getSignalsTime(firstSignalSide, organisedEmaValues)
        return signals
