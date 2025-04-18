class Config:
    def __init__(self):
        self.daysOfEma = [5,8,13]
        self.years = [2020, 2021, 2022, 2023, 2024]
        self.months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        self.buyPointsGap = 0.005  #Yüzde olarak ne kadar az ve ya çok aralığı
        self.buyPointsCount = 20  #Toplam kaç adet işlem yapılacağı
        self.totalEntryAmount = 12000
        self.seperatedMoneyAmount = 150
        self._settingsStages()
        self._stage3PhasesGaps()
        self._pandasConfig()

    def _settingsStages(self):  #Değerler yüzde olarak verilmiştir.
        self.stopLossPnl = -0.2
        self.entryStopPnl = 0.04
        #Porsiyon değerleri yüzde olarak verilmiştir. 3 stage in porsiyon oranlarının toplamı 1 olmak zorundadır.
        self.stage1SellPortion = 0.5  #Ana işlemde stage 1'de satış yapılırken kullanılacak satış oranı 
        self.stage2SellPortion = 0.25 #Ana işlemde stage 2'de satış yapılırken kullanılacak satış oranı 
        self.stage3SellPortion = 0.25 #Ana işlemde stage 3'de satış yapılırken kullanılacak satış oranı 
        self.stage1StartPnl = 0.3
        self.stage2StartPnl = 0.5
        self.stage3StartPnl = 1
        self.increaseStopPoint1Pnl = 0.19
        self.increaseStopPoint2Pnl = 0.34
        self.increaseStopPoint3Pnl = 0.54

    def _stage3PhasesGaps(self):
        self.gap1 = 0.65 #Stage 3 başlama noktasından bu değere kadar increaseStopPoint1 devrede
        self.gap2 = 0.8 #gap1 değerinden bu değere kadar increaseStopPoint2 devrede ve bu değerin üstünde increaseStopPoint3 devrede. 

    def _pandasConfig(self):
        self.COLUMN_NAMES = ['OpenTime', 'Open', 'High', 'Low', 'Close', 'Volume', 
                    'CloseTime', 'QuoteAssetVolume', 'NumberOfTrades', 
                    'TakerBuyBaseAssetVolume', 'TakerBuyQuoteAssetVolume', 'Ignore']
        self.cleanRowCount = 30


