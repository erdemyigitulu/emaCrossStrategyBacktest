import json
from services.signal_service import SignalService
from helpers.utils import Utils
from helpers.stage_controller import StageController        
from data_access.candles_data_access import CandlesDataAccess
from src.config import Config
from services.data_processor import DataProcessor
from services.engine import Engine



class BacktestService:
    def __init__(self):
        self.signal_service = SignalService()
        self.candles_data_access = CandlesDataAccess ()
        self.data_processor = DataProcessor()
        self.utils = Utils()
        self.config = Config()
        self.stage_controller = StageController()



    def startBacktest(self):
        years = self.config.years
        months = self.config.months
        for year in years:
            for month in months:
                signals = self.signal_service.extractSignals(month, year)
                data1s = self.utils.get1sData(month, year)
                for index, signal in enumerate(signals[1:]):
                    self.stage_controller.stage1Activator()
                    try:
                        nextSignal = signals[(index + 2)][1]
                    except:
                        break
                    engine = Engine()
                    engine.pushSignalData(signal , data1s)
                    for _1sdata in data1s[engine.startIndex:]:
                        engine.findpurhasedProcessesData()
                        engine.pushVariableValues(_1sdata)
                        if self.stage_controller.stage1isActivated:
                            engine.stage1()
                        if self.stage_controller.stage2isActivated:
                            engine.stage2()
                        if self.stage_controller.stage3isActivated:
                            engine.stage3()
                        engine.engineAlgoritm()
                        if engine.closeEngine :
                            break
                        if currentTimeStamp > nextSignal + 900000:
                            print("yeni sinyal geldiği için işlemi kapatıyorumke")
                            profitLoss = moneyProfitLossFunc(profitLoss, self.totalAmount, engine.pnL, portion)
                            message = "yeni sinyal geldiği için işlemi kapatıyorumke"
                            messages.append(message)
                            resultDatas.append(
                                {
                                    "signal": signalSide,
                                    "signalTimeStamp": signal[1],
                                    "startProcessTimestamp": startProcessTimestamp,
                                    "profitLoss": profitLoss,
                                    "self.totalAmount": self.totalAmount,
                                }
                            )
                            break
                        if a:
                            print("Stage1 başladı")
                            a = False
                        if engine.pnL >= 0.2 and b:
                            engine.stage2Start = True
                            print("Stage2 başladı")
                            b = False
                        if engine.pnL >= 0.5 and c:
                            engine.stage3Start = True
                            print("Stage3 başladı")
                            c = False

                    if profitLoss < 0:
                        loss = loss + profitLoss
                        lossesCount = lossesCount + 1
                    elif profitLoss > 0:
                        profit = profit + profitLoss
                        profitsCount = profitsCount + 1
                    else:
                        entryStopsCount = entryStopsCount + 1

                    totalpnL = totalpnL + profitLoss
                    purchasedPoints = "".join(
                        [f"({x[0]}, {x[1]})" for x in purchasedPoints]
                    )
                    resultDatas[-1]["processEndTimeStamp"] = currentTimeStamp
                    resultDatas[-1]["purchasedPoints"] = purchasedPoints
                    resultDatas[-1]["situationOfProcess"] = messages
                    resultDatas[-1]["totalPnL"] = totalpnL
                    resultDatas[-1]["totalProfit"] = (profit, profitsCount)
                    resultDatas[-1]["totalLoss"] = (loss, lossesCount)
                    resultDatas[-1]["totalEntryStop"] = entryStopsCount

                    with open(resultscsv, "w", encoding="utf-8") as json_file:
                        json.dump(
                            resultDatas,
                            json_file,
                            indent=4,
                            separators=(",", ": "),
                            ensure_ascii=False,
                        )
