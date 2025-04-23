import numpy as np
from services.data_converter import DataConverter

class CarryOverManager:
    def __init__(self, data_converter:DataConverter):
        self.data_converter = data_converter
        self.isCarryOver = False

    def prepareCarryOverData(self, carrySignal, currentMonth, currentYear):
        if currentMonth == 1:
            prevMonth = 12
            prevYear = currentYear - 1
        else:
            prevMonth = currentMonth - 1
            prevYear = currentYear

        prev1s = self.data_converter.get1sData(prevMonth, prevYear)
        current1s = self.data_converter.get1sData(currentMonth, currentYear)

        startTs = int(carrySignal[1]) + 900_000 
        tailFromPrev = prev1s[prev1s[:, 0] >= startTs]
        combined1s = np.concatenate([tailFromPrev, current1s], axis=0)
        return combined1s

