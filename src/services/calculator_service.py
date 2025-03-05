class CalculaterService:
    def __calculateEma(dataOfEma, day):
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

    def calculateAvaregePrice(islemler):
        totalCost = sum(fiyat * miktar for fiyat, miktar in islemler)
        totalAmount = sum(miktar for _, miktar in islemler)
        ortalama = totalCost / totalAmount
        return ortalama, totalAmount

    def calculatingCurrentEma(timeStamp, price, signal):
        with open(main15mcsv) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=",")
            datas = []
            for row in csv_reader:
                data = {"timeStamp": int(row[0]), "closeTime": float(row[4])}
                datas.append(data)
            csv_file.close()
        for index, data in enumerate(datas):
            datatimestamp = timeStamp - data["timeStamp"]
            if datatimestamp < 0:
                del datas[index - 1 :]
                break
        datas.append({"timeStamp": timeStamp, "closeTime": price})
        emaDataOfDay = calculateEma(datas, 5)
        emaDatas = [emaDataOfDay[-2], emaDataOfDay[-1]]
        if signal == "short":
            emaDatas = list(map(lambda x: -1 * x, emaDatas))
        if emaDatas[-1] < emaDatas[-2]:
            protectProcess = True
        return protectProcess

    def calculateEmaValues(self, closeTimes):
        dayOfEma = [5, 8, 13]
        emaDatasOfDays = []
        for day in dayOfEma:
            emaDataOfDay = self.__calculateEma(closeTimes, day)
            emaDatasOfDays.append(emaDataOfDay)
        return emaDatasOfDays
