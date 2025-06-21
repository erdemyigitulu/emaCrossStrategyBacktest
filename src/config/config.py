class Config:
    def __init__(self):
        self.daysOfEma = [5,8,13]
        self.years = [2021, 2022, 2023, 2024]
        self.months = [7, 8, 9, 10, 11, 12]
        self.buyPointsGap = 0.005  #Yüzde olarak ne kadar az ve ya çok aralığı
        self.buyPointsCount = 20  #Toplam kaç adet işlem yapılacağı
        self.totalEntryAmount = 12000
        self.seperatedMoneyAmount = 150
        self._settingsStages()
        self._pandasConfig()
        self._indicatorsData()
        self._stage_flow()

    def _settingsStages(self):  #Değerler yüzde olarak verilmiştir.
        #Porsiyon değerleri yüzde olarak verilmiştir. 3 aşamanın porsiyon oranlarının toplamı 1 olmak zorundadır.
        self.stage1SellPortion = 0.5  #Ana işlemde stage 1'de satış yapılırken kullanılacak satış oranı 
        self.stage2SellPortion = 0.25 #Ana işlemde stage 2'de satış yapılırken kullanılacak satış oranı 
        self.stage3SellPortion = 0.25 #Ana işlemde stage 3'de satış yapılırken kullanılacak satış oranı 

    def _pandasConfig(self):
        self.COLUMN_NAMES = ['OpenTime', 'Open', 'High', 'Low', 'Close', 'Volume', 
                    'CloseTime', 'QuoteAssetVolume', 'NumberOfTrades', 
                    'TakerBuyBaseAssetVolume', 'TakerBuyQuoteAssetVolume', 'Ignore']
        self.cleanRowCount = 30

    def _indicatorsData(self):
        self.INDICATOR_MAP = {
        "ExponentialMovingAverageIndicator": "indicators.exponantional_moving_average",
        "AverageTrueRangeIndicator": "indicators.average_true_range"
    }
        self.USED_INDICATORS = [
        "ExponentialMovingAverageIndicator",
        "AverageTrueRangeIndicator"
    ]

    def _stage_flow(self):  
        self.STAGE_FLOW = [
        {
            "main": "stage1",
            "first": {
                "pnl_key": "stage1StartPnl",
                "pnl_value": 0.2,
                "shouldClose": False,
                "sell" : True,
                "sell_portion" : 0.5
            },
            "second": {
                "pnl_key": "stopLossPnl",
                "pnl_value": -0.2,
                "shouldClose": True,
                "sell" : True,
                "sell_portion" : 1
            }
        },
        {
            "main": "stage2",
            "first": {
                "pnl_key": "stage2StartPnl",
                "pnl_value": 0.5,
                "shouldClose": False,
                "sell" : True,
                "sell_portion" : 0.25
            },
            "second": {
                "pnl_key": "entryStopPnl",
                "pnl_value": 0.04,
                "shouldClose": True,
                "sell" : True,
                "sell_portion" : 1
            }
        },
        {
            "main": "stage3inphase1",
            "first": {
                "pnl_key": "stage3inphase1",
                "pnl_value": 0.65,
                "shouldClose": False,
                "sell" : False,
                "sell_portion" : None
            },
            "second": {
                "pnl_key": "increaseStopPoint1Pnl",
                "pnl_value": 0.19,
                "shouldClose": True,
                "sell" : True,
                "sell_portion" : 1
                
            }
        },
        {
            "main": "stage3inphase2",
            "first": {
                "pnl_key": "stage3inphase2",
                "pnl_value": 0.8,
                "shouldClose": False,
                "sell" : False,
                "sell_portion" : None
            },
            "second": {
                "pnl_key": "increaseStopPoint2Pnl",
                "pnl_value": 0.35,
                "shouldClose": True,
                "sell" : True,
                "sell_portion" : 1
            }
        },
        {
            "main": "stage3inphase3",
            "first": {
                "pnl_key": "stage3",
                "pnl_value": 1,
                "shouldClose": True,
                "sell" : True,
                "sell_portion" : 1
            },
            "second": {
                "pnl_key": "increaseStopPoint2Pnl",
                "pnl_value": 0.54,
                "shouldClose": True,
                "sell" : True,
                "sell_portion" : 1
            }
        }
    ]
