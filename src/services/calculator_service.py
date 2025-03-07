from config import Config


class CalculaterService:

    def __init__ (self):
        self.config = Config()

    def calculateEma(dataOfEma, day):
        data = []
        for closetime in dataOfEma:
            close = closetime["closeTime"]
            data.append(close)
        emaValues = []
        multiplier = 2 / (day + 1)
        initialEma = sum(data[:day]) / day
        emaValues.append(initialEma)
        for i in range(day, len(data)):
            ema = (data[i] - emaValues[-1]) * multiplier + emaValues[-1]
            emaValues.append(ema)
        return emaValues

    def calculateAvaregePrice(processes):
        totalCost = sum(price * amount for price, amount in processes)
        totalAmount = sum(amount for _, amount in processes)
        average = totalCost / totalAmount
        return average, totalAmount

    def percentageIncrease(firstValue, SecondValue, signal):
        percentage = ((SecondValue - firstValue) / firstValue) * 100
        percentage = round(percentage, 2)
        if signal == "short":
            percentage = -(percentage)
        return percentage

    def moneyProfitLossFunc(profitLoss, money, pnL, portion):
        if profitLoss == 0:
            profitLoss = ((money * (100 + pnL) / 100) - money) * portion
            print(profitLoss)
        else:
            profitLoss = profitLoss + ((money * (100 + pnL) / 100) - money) * portion
            print(profitLoss)
        print(profitLoss, money, pnL, portion)
        return profitLoss

    # def calculatingCurrentEma(self , timeStamp, price, signal):
    #     with open(main15mcsv) as csv_file:
    #         csv_reader = csv.reader(csv_file, delimiter=",")
    #         datas = []
    #         for row in csv_reader:
    #             data = {"timeStamp": int(row[0]), "closeTime": float(row[4])}
    #             datas.append(data)
    #         csv_file.close()
    #     for index, data in enumerate(datas):
    #         datatimestamp = timeStamp - data["timeStamp"]
    #         if datatimestamp < 0:
    #             del datas[index - 1 :]
    #             break
    #     datas.append({"timeStamp": timeStamp, "closeTime": price})
    #     emaDataOfDay = self.calculateEma(datas, 5)
    #     emaDatas = [emaDataOfDay[-2], emaDataOfDay[-1]]
    #     if signal == "short":
    #         emaDatas = list(map(lambda x: -1 * x, emaDatas))
    #     if emaDatas[-1] < emaDatas[-2]:
    #         protectProcess = True
    #     return protectProcess

